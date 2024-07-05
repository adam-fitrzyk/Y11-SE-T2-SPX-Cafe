from Avatar import Avatar
from Customer import Customer
from NLPDemo import NLPDemo
from time import time

class Chatbot(Avatar):

    def __init__(self):
        super().__init__()
        self.nlp = NLPDemo()
        self.say("Welcome to Chatbot 2.0!")

    def getCustomer(self):
        self.user_name = self.listen("Please enter your username: ", use_sr=False)
        self.say(f"Ok. Checking your username: {self.user_name}. Please wait...")
        self.customer = Customer.findUser(self.user_name)
        if self.customer:
            self.say(f"Welcome back {self.customer.getName()}!")
            return
        else:
            self.getName()
            self.customer = Customer(self.user_name, self.first_name, self.last_name)

            

    def getName(self):
        inp_name = self.listen("Please tell me your first name?", phrase_time_limit=5)
        self.first_name = self.nlp.getNamesByPartsOfSpeech(inp_name)
        inp_name = self.listen("Please tell me your last name?", phrase_time_limit=5)
        self.last_name = self.nlp.getNamesByPartsOfSpeech(inp_name)
        self.say(f"Hello {self.first_name} {self.last_name}! How are you today?")


def main():
    #st1 = round(time())
    c = Chatbot()
    #et1 = round(time())
    #print(f"{et1-st1} seconds to run")
    c.getCustomer()

if __name__ == "__main__":
    main()