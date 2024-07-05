from Avatar import Avatar
from Menu import Menu
from Customer import Customer
#from NLPDemo import NLPDemo
from rapidfuzz.fuzz import partial_ratio
from rapidfuzz.utils import default_process
from rapidfuzz.process import extract

class Chatbot:

    def __init__(self):
        '''Constructor Method for Chatbot class '''
        self.menu = Menu("Italia Forever Lunch Menu")
        self.exit_request = {
            "keywords": ["exit", "leave", "bye"],
            "response": "leave us now"
        }
        self.order_request = {
            "keywords": ["order", "buy", "pay"],
            "response": "order food"
        }
        self.menu_request = {
            "keywords": ["menu", "see food"],
            "response": "see the menu"
        }
        self.history_request = {
            "keywords": ["history", "previous", "past"],
            "response": "see order history"
        }
        self.options = {
            "exit":     self.exit_request,
            "order":    self.order_request,
            "menu":     self.order_request,
            "history":  self.history_request
        }
        self.waiter = Avatar("Luigi")
        self.waiter.say("Welcome to Italiabot.")

    def matchOptions(self, choice):
        '''Choose best match from a list of options '''
        retlist = []
        matches = []
        max_confidence = 0
        is_exit = False
        is_order = False
        is_menu = False
        is_history = False

        keywords = [self.options[key]["keywords"] for key in self.options]
        keywords = keywords[0] + keywords[1] + keywords[2] + keywords[3]

        results = extract(choice, keywords, processor=default_process)
        for result in results:
            (match, confidence, index) = result
            print(f"Checking: {result}")
            if confidence > max_confidence and confidence > 80:
                max_confidence = confidence
                matches = [match]
            elif confidence == max_confidence:
                matches.append(match)

        print(f"You have matched: {', '.join(matches)} with confidence level {max_confidence}%")
        for keyword in self.exit_request["keywords"]:
            if keyword in matches:
                retlist.append("leave")
        for keyword in self.menu_request["keywords"]:
            if keyword in matches:
                retlist.append("menu")
        for keyword in self.order_request["keywords"]:
            if keyword in matches:
                retlist.append("order")
        for keyword in self.history_request["keywords"]:
            if keyword in matches:
                retlist.append("history")

        if len(retlist) > 1:
            self.waiter.say(f"Did you mean {', or '.join(retlist)}? Please try again.")
        elif retlist:
            return retlist[0]
        else:
            return None
        
    def getRequest(self):
        response = None
        self.waiter.say(f"Ok {self.customer.getFirstName()}. What would you like to do? Order food? See the menu? Look at your order history? Or exit?")
        while not response:
            print("Order food, see the menu, look at your order history, or exit?")
            option = self.waiter.listen(None, phrase_time_limit=5)
            response = self.matchOptions(option)
        match response:
            case "exit":
                self.waiter.say(f"You chose to: {self.options["exit"]["response"]}. Thank you, {self.customer.getFirstName()}, for ordering with Italiabot today. Goodbye")
            case "menu":
                self.waiter.say(f"You chose to: {self.options["menu"]["response"]}")
            case "order":
                self.waiter.say(f"You chose to: {self.options["order"]["response"]}")
            case "history":
                self.waiter.say(f"You chose to: {self.options["history"]["response"]}")
        return response
        
    def getCustomer(self):
        '''Get a customer - using username typed in for accuracy '''
        print("Italiabot")
        username = self.waiter.listen("Please enter your username", use_sr=False)
        print("... Checking our customer database...")
        # look up customer -> new customer or welcome back
        self.customer = Customer(username)
        
        self.waiter.say(f"Welcome {self.customer.getFirstName()} {self.customer.getLastName()}")

    def displayOrderHistory(self):
        self.waiter.say(f"Ok, {self.customer.getFirstName()}. Let's show you your previous orders.")

    def displayMenu(self):
        self.waiter.say(f"Alright, {self.customer.getFirstName()}. Let's show you the menu.")
        self.menu.display()

    def orderFood(self):
        self.waiter.say(f"Prego, {self.customer.getFirstName()}. Let's order some food.")

    def run(self):
        # Get the customer
        self.getCustomer()

        #LOOP - 1) Order? 2) View Menu? 3) Order History 4) Leave
        running = True
        while running:
            choice = self.getRequest()
            print(choice)

            if choice == "exit":
                running = False
            elif choice == "history":
                self.displayOrderHistory()
            elif choice == "menu":
                self.displayMenu()
            elif choice == "order":
                self.orderFood()

def main():
    italiabot = Chatbot()

    italiabot.run()

if __name__ == "__main__":
    main()