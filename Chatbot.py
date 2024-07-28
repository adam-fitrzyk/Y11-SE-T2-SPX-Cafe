from Avatar import Avatar
from Menu import Menu
from Customer import Customer
from NLPDemo import NLPDemo
from rapidfuzz.utils import default_process
from rapidfuzz.process import extract

class Chatbot:

    def __init__(self, name, menu_name, cafe_name) -> None:
        '''Constructor Method for Chatbot class '''
        self.nlp = NLPDemo()
        self.__waiter = Avatar(name)
        self.__menu = Menu(menu_name)
        self.cafe_name = cafe_name
        self.exit_request = {
            "keywords": ["exit", "leave", "quit"],
            "response": "leave us now"
        }
        self.order_request = {
            "keywords": ["order", "buy", "pay"],
            "response": "order food"
        }
        self.menu_request = {
            "keywords": ["menu"],
            "response": "see the menu"
        }
        self.history_request = {
            "keywords": ["order history", "previous", "past"],
            "response": "see order history"
        }
        self.options = {
            "exit":     self.exit_request,
            "order":    self.order_request,
            "menu":     self.menu_request,
            "history":  self.history_request
        }
        keywords = [self.options[key]["keywords"] for key in self.options]
        self.keywords = keywords[0] + keywords[1] + keywords[2] + keywords[3]

         
    def getCustomer(self) -> None:
        '''Get a customer - using username typed in for accuracy '''
        print(self.cafe_name, "Bot")
        username = self.__waiter.listen("Please enter your username", use_sr=False)
        print("... Checking our customer database ...")
        # look up customer -> new customer or welcome back
        customer_id = Customer.findUser(username)
        if customer_id:
            self.__customer = Customer(customerId=customer_id)
            self.welcomeCustomer(self.__customer.getName())
        else:
            self.welcomeCustomer()
            first_name = None
            last_name = None
            while not first_name:
                inp_name = self.__waiter.listen("Please tell me your first name?", phrase_time_limit=5)
                first_name = self.nlp.getNamesByPartsOfSpeech(inp_name)
            while not last_name:
                inp_name = self.__waiter.listen("Please tell me your last name?", phrase_time_limit=5)
                last_name = self.nlp.getNamesByPartsOfSpeech(inp_name)
            self.__customer = Customer(username=username, firstname=first_name, lastname=last_name)

    def matchOptions(self, choice) -> list[str] | None:
        '''Choose best match from a list of options, returns None unless only one option is matched. '''
        retlist = set()
        matches = []
        max_confidence = 0

        results = extract(choice, self.keywords, processor=default_process)
        for result in results:
            (match, confidence, index) = result
            print(f"Checking: {result}")
            if confidence > max_confidence and confidence > 80:
                max_confidence = confidence
                matches = [match]
            elif confidence == max_confidence:
                matches.append(match)

        print(f"You have matched: {', '.join(matches)} with confidence level {max_confidence}%")

        for match in matches:
            if match in self.exit_request["keywords"]:
                retlist.add("exit")
            elif match in self.menu_request["keywords"]:
                retlist.add("menu")
            elif match in self.order_request["keywords"]:
                retlist.add("order")
            elif match in self.history_request["keywords"]:
                retlist.add("history")
                
        if len(retlist) > 1:
            self.__waiter.say(f"Did you mean {', or '.join(retlist)}? Please try again.")
        elif retlist:
            return list(retlist)[0]
        
    def getRequest(self) -> str:
        '''Keep asking the customer to choose an option until they choose just one. '''
        response = None
        self.__waiter.say(f"Ok {self.__customer.getFirstName()}. Tell me what would you like to do... Order food, see the menu, look at your order history, or exit?")
        while not response:
            print("Order food, see the menu, look at your order history, or exit?")
            option = self.__waiter.listen(None, phrase_time_limit=5)
            response = self.matchOptions(option)
        self.__waiter.say(f"You chose to: {self.options[response]["response"]}")
        if response == "exit":
            self.__waiter.say(f"Thank you, {self.__customer.getFirstName()}, for ordering with {self.cafe_name}-bot today! Doh-vee-jeh-nia.")
        return response

    def displayOrderHistory(self):
        self.__waiter.say(f"Ok, {self.__customer.getFirstName()}. Let's show you your previous orders.")
        self.__customer.displayOrders()

    def displayMenu(self):
        self.__waiter.say(f"Alright, {self.__customer.getFirstName()}. Let's show you the menu.")
        self.__menu.display()

    def orderFood(self):
        self.__waiter.say(f"Dob-jeh, {self.__customer.getFirstName()}. Let's order some food.")
        pass

    def welcomeCustomer(self, name=''):
        self.__waiter.say(f"Jen dough-bray {name}! Welcome to {self.cafe_name}!") # Jen dough-bray -> Dzien dobry -> Good day

    def run(self):
        # Get the customer
        self.getCustomer()

        #LOOP - 1) Order? 2) View Menu? 3) Order History 4) Leave
        running = True
        while running:
            choice = self.getRequest()

            if choice == "exit":
                running = False
            elif choice == "history":
                self.displayOrderHistory()
                input("Enter anything to go back: ")
            elif choice == "menu":
                self.displayMenu()
                input("Enter anything to go back: ")
            elif choice == "order":
                self.orderFood()
                input("Enter anything to go back: ")

def main():
    polabot = Chatbot("Agata", "Polander Plates", "Polander Plains")

    polabot.run()

if __name__ == "__main__":
    main()