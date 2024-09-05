import pyttsx4 as Tts
import speech_recognition as Sr

# Our Avatar is responsible for:
# 1. Saying things - using text to speech
# 2. Listening for things - using Speech Recognition
#
# It has its own personal instance data:
# 1. Name
# 2. Useful things for system functions

# -------------------------------------------------------------------
# We use Text to Speech and Speech Recognition

class Avatar:
    def __init__(self, name='Hazel Brown Eaze') -> None: # constructor method
        self.name = name
        self.initVoice()
        self.initSR()
        self.introduce()

    def initSR(self) -> None:
        self.sample_rate = 48000
        self.chunk_size = 2048
        self.sr = Sr.Recognizer()
        self.use_sr = True

    def initVoice(self) -> None:
        """
        Method: Initialize Text to Speech
        """
        self.__engine = Tts.init()
        self.__voices = self.__engine.getProperty('voices')
        self.__vix = 0
        self.__voice = self.__voices[self.__vix].id
        self.__engine.setProperty('voice', self.__voice)
        self.__engine.setProperty('rate', 150)
        self.__engine.setProperty('volume', 1.0)

    def say(self, speech):
        self.__engine.say(speech, self.name)
        self.__engine.runAndWait()

    def listen(self, prompt="I am listening, please speak", use_sr=None, phrase_time_limit=10):
        speech = ""
        if use_sr == None:
            use_sr = self.use_sr
        if use_sr:
            try:
                with Sr.Microphone(device_index=0, sample_rate=self.sample_rate, chunk_size=self.chunk_size) as source:
                    # listen for 1 second to calibrate the energy threshold for ambient noise levels
                    self.sr.adjust_for_ambient_noise(source)
                    self.say(prompt)
                    audio = self.sr.listen(source, 5, phrase_time_limit)
                try:
                    speech = self.sr.recognize_google(audio)
                    print(f"You said: '{speech}'")
                except Sr.UnknownValueError:
                    self.say("Sorry I did not catch that.")
                except Sr.RequestError as e:
                    self.say(f"Could not request results; {e}")
            except:
                self.say(prompt)
                speech = input(prompt+": ")
        else:
            self.say(prompt)
            speech = input(prompt+": ")
        return speech
    
    def introduce(self) -> None:
        self.say(f"Hello. My name is {self.name}")

# This is our test harness
def main():
    teacher = Avatar('Bob')

    teacher.listen("say a number")

if __name__ == "__main__":
    main()