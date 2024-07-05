from SPXCafe import SPXCafe
from Avatar import Avatar
from Customer import Customer
from Menu import Menu
from NLPDemo import NLPDemo
from rapidfuzz import fuzz, process, utils
from rapidfuzz.fuzz import partial_ratio

class Cafe(SPXCafe):

    def __init__(self, cafe_name=None) -> None:
        super().__init__()
        self.waiter = Avatar("Luigi")
        self.setCafeName(cafe_name)
        self.menu = Menu('Dinner Menu')

    def setCafeName(self, cafe_name) -> None:
        if cafe_name:
            self.cafe_name = cafe_name
        else:
            self.cafe_name = 'Italia Corner'

    def getCafeName(self) -> str:
        return

    def welcomeCustomer(self):
        self.waiter.say(f"Buon Giorno! Welcome to {self.getCafeName()}")

        while True:
            #user_name = self.waiter.listen("Can you please enter your username? ", use_sr=False)
            user_name = 'bloggs'
            self.customer = Customer(user_name)
            is_customer = None
            self.waiter.say(f"Welcome back {self.customer.getFirstName()}!")
            break


def main() -> None:
    pass

if __name__ == "__main__":
    main()