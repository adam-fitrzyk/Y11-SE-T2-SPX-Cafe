import pyttsx4 as Ptts
import speech_recognition as Sr
import pyaudio as Pa
import wave
import sys

class Avatar:
    def init_voice(self):

        self.__engine = Ptts.init()
        self.__voices = self.__engine.getProperty('voices')
        self.__vix = 1
        self.__voice = self.__voices[self.__vix]

def speak() -> None:
    engine = Ptts.init()
    engine_voices = engine.getProperty('voices')
    voices = {'hazel': engine_voices[0].id, 'zira': engine_voices[1].id}
    engine.setProperty('voice', voices['hazel'])

    engine.say('say something im waiting.')
    engine.runAndWait()

def listen():
    r = Sr.Recognizer()
    mic = Sr.Microphone(device_index=0)
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 5)
        try:
            speech = r.recognize_google(audio)
            print(f"You said: {speech}")
        except:
            print("Sorry I didn't catch that.")


"""
with wave.open(sys.argv[1], 'rb') as wf:
    # Instantiate PyAudio and initialize PortAudio system resources (1)
    pa = Pa.PyAudio()

    # Open stream (2)
    stream = pa.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
"""

def main() -> None:
    speak()

if __name__ == "__main__":
    main()