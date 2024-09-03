from SPXCafe import SPXCafe
from Chatbot import Chatbot
from Customer import Customer
from Menu import Menu
from NLPDemo import NLPDemo
from rapidfuzz import fuzz, process, utils
from rapidfuzz.fuzz import partial_ratio

class Cafe(SPXCafe):

    def __init__(self, cafe_name=None, menu_name=None, waiter_name=None) -> None:
        super().__init__()
        self.setCafeName(cafe_name)
        self.setChatbot(waiter_name, menu_name, self.getCafeName())

    def setChatbot(self, waiter_name, menu_name):
        if not waiter_name:
            waiter_name = "Agata"
        if not menu_name:
            menu_name = "Polander Plates"
        self.__chatbot = Chatbot(waiter_name, menu_name)

    def setCafeName(self, cafe_name) -> None:
        if cafe_name:
            self.__cafe_name = cafe_name
        else:
            self.__cafe_name = 'Polander Plains'

    def getCafeName(self) -> str:
        return self.__cafe_name
    
    def run(self):
        pass


def main() -> None:
    pass

if __name__ == "__main__":
    main()