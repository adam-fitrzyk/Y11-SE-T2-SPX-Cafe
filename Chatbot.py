from Avatar import Avatar
from Menu import Menu
from Customer import Customer
from NLPDemo import NLPDemo
from Orders import Order, OrderItem
from rapidfuzz.utils import default_process
from rapidfuzz.process import extract
from word2number.w2n import american_number_system

use_sr = False
phrase_time_limit = 5

class Chatbot:

    def __init__(self, name, menu_name, cafe_name) -> None:
        '''Constructor Method for Chatbot class '''
        self.__nlp = NLPDemo()
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
            "response": "see your order history"
        }
        self.main_options = {
            "menu":     self.menu_request,
            "order":    self.order_request,
            "history":  self.history_request,
            "exit":     self.exit_request
        }
        courseobjs = self.__menu.get_courses()
        courses = [course.get_course_name() for course in courseobjs]
        self.course_options = {}
        self.meal_options = {}
        # Create dictionary for interpretting commands and 
        for course in courses:
            self.course_options[course] = {"keywords": [course], "response": f"see {course} options"}
        self.course_options["checkout"] = {"keywords": ['complete', 'submit', 'finish', 'checkout'], "response": "go to checkout"}
        self.course_options["abandon"] = {"keywords": ["abandon", "exit", "leave", "go back"], "response": "abandon order"}
        for course in courseobjs:
            course_meal_options = {}
            for meal in course.get_meals():
                course_meal_options[meal.get_meal_name()] = {
                    "keywords": [meal.get_meal_name()], 
                    "response": f"order {meal.get_meal_name()}"
                }
            course_meal_options["back"] = {"keywords": ["go back", "nevermind", "see courses"], "response": "go back to courses"}
            course_meal_options["checkout"] = {"keywords": ['complete', 'submit', 'finish', 'checkout'], "response": "go to checkout"}
            course_meal_options["abandon"] = {"keywords": ["abandon", "exit", "leave"], "response": "abandon order"}
            self.meal_options[course.get_course_name()] = course_meal_options
        
        self.yes_no_options = {"yes": {'keywords': ["yes"], 'response': "yes"}, "no": {'keywords': ["no", "n't"], 'response': "no"}}
        
    def getCustomer(self) -> None:
        '''Get a customer - using username typed in for accuracy '''
        print(self.cafe_name, "Bot")

        response = None
        prompt = "Are you an existing customer?"
        while not response:
            speech = self.__waiter.listen(prompt, use_sr, phrase_time_limit)
            response = self.matchOptions(speech, self.yes_no_options)
        existing_customer = True if response == 'yes' else False
        
        if existing_customer:
            customer_id = None
            while customer_id == None:
                username = self.__waiter.listen("Please enter your username", use_sr=False)
                print("... Checking our customer database ...")
                # look up customer -> new customer or welcome back
                customer_id = Customer.findUser(username)
                if customer_id:
                    self.__customer = Customer(customerId=customer_id)
                    self.welcomeCustomer(self.__customer.getName())
                else:
                    self.__waiter.say(f"I'm sorry, I couldn't find {username} in our database. Please re-enter your username.")
        else:
            self.welcomeCustomer()
            first_name = None
            last_name = None
            while not first_name:
                inp_name = self.__waiter.listen("Please tell me your first name?", phrase_time_limit=phrase_time_limit, use_sr=use_sr)
                first_name = self.__nlp.getNamesByPartsOfSpeech(inp_name)
            while not last_name:
                inp_name = self.__waiter.listen("Please tell me your last name?", phrase_time_limit=phrase_time_limit, use_sr=use_sr)
                last_name = self.__nlp.getNamesByPartsOfSpeech(inp_name)
            self.__customer = Customer(username=username, firstname=first_name, lastname=last_name)

    def matchOptions(self, choice:str, options:dict[str: dict[str: list[str] | str]]) -> str | None:
        '''Choose best match from options, a dictionary:
        >> dict[str: dict['keywords': list[str], 'response': str]] <<\n
        and returns None unless only one option is matched. '''
        retlist = set()
        matches = []
        max_confidence = 0
        keywords = []
        items = [options[option]["keywords"] for option in options]
        for item in items:
            keywords += item

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

        for match in matches:
            for option in options:
                if match in options[option]["keywords"]:
                    retlist.add(option)

        if len(retlist) > 1:
            self.__waiter.say(f"Did you mean {', or '.join(retlist)}? Please try again.")
        elif retlist:
            return list(retlist)[0]

    def getRequest(self, options, prompt) -> str:
        '''Keep asking the customer to choose an option until they choose just one. '''
        response = None
        self.__waiter.say(f"Ok {self.__customer.getFirstName()}. {prompt}?")
        while not response:
            print(f"> {prompt}?")
            option = self.__waiter.listen('', phrase_time_limit=phrase_time_limit, use_sr=use_sr)
            response = self.matchOptions(option, options)
        self.__waiter.say(f"You chose: {options[response]["response"]}")
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
        ordering = True
        # Loop - until customer doesn't want to order anything
        while ordering:
            order = Order(customerId=self.__customer.getCustomerId())
            valid_order = True
            asking_course = True

            # Ask which course customer wants to order from
            while asking_course:
                asking_meal = True
                course_choice = self.askCourse()
                if course_choice == 'ABANDON':
                    asking_course, asking_meal, valid_order = False, False, False
                elif course_choice == 'CHECKOUT':
                    asking_course, asking_meal = False, False
                
                # Ask what meal customer wants to order, add to the order
                while asking_meal:
                    course_choice.display()
                    meal_choice, quantity = self.askMeal(course_choice)
                    if meal_choice == 'ABANDON':
                        asking_course, valid_order = False, False
                        break
                    elif meal_choice == 'CHECKOUT':
                        asking_course = False
                        break
                    if meal_choice == 'BACK':
                        break

                    print(meal_choice, quantity)
                    self.__waiter.say(f"You chose to: {self.meal_options[course_choice.get_course_name()][meal_choice.get_meal_name()]["response"]} {quantity} times.")

                    order.placeItem(meal_choice.get_meal_id(), quantity)

                    # Ask if customer wants to order another meal
                    prompt = "Would you like to order another meal"
                    order_another_meal = self.getRequest(self.yes_no_options, prompt)
                    if order_another_meal == "no":
                        asking_meal = False

            print('-'*5 + 'Basket' + '-'*5)
            order.display()
            if valid_order:
                prompt = "Are you sure you would like to checkout"
                checkout = self.getRequest(self.yes_no_options, prompt)
                if checkout == 'yes':
                    order.save()
                    self.__customer.addOrder(order)

            prompt = "Would you like to make another order"
            order_again = self.getRequest(self.yes_no_options, prompt)
            if order_again == 'no':
                ordering = False

    def askCourse(self):
        ''''''
        self.__menu.display_courses()
        prompt = "Which course would you like to order from? Otherwise you can abandon or checkout"
        choice = self.getRequest(self.course_options, prompt)
        if choice == "abandon":
            return 'ABANDON'
        elif choice == "checkout":
            return 'CHECKOUT'
        course = self.__menu.find_course(choice)[0]
        return course

    def askMeal(self, course):
        ''''''
        choice, number = None, None
        while not choice and not number:
            if not choice:
                speech = self.__waiter.listen(f"Which meal would you like to order? Otherwise would you like to abandon or submit your order?", phrase_time_limit=phrase_time_limit, use_sr=use_sr)
                choice = self.matchOptions(speech, self.meal_options[course.get_course_name()])
                number = self.__nlp.getNumbersByPartsOfSpeech(speech)
                meal = self.__menu.find_meal(self.__nlp.getNounsByPartsOfSpeech(speech))[0]
            if choice == "abandon":
                return 'ABANDON', 0
            elif choice == "checkout":
                return 'CHECKOUT', 0
            elif choice == "back":
                return 'BACK', 0
            if meal and not number:
                while not number:
                    speech = self.__waiter.listen(f"How many of the {meal.get_meal_name()} would you like?", phrase_time_limit=phrase_time_limit, use_sr=use_sr)
                    number = self.__nlp.getNumbersByPartsOfSpeech(speech)
            if meal:
                confirmed = None
                while confirmed == None:
                    speech = self.__waiter.listen(f"Are you sure you would like to order {meal.get_meal_name()}?", phrase_time_limit=phrase_time_limit, use_sr=use_sr)
                    confirmed = self.matchOptions(speech, self.yes_no_options)
                confirmed = True if confirmed == 'yes' else False
                if not confirmed:
                    choice = None
        quantity = american_number_system[number[0]]
        return meal, quantity

    def welcomeCustomer(self, name=''):
        self.__waiter.say(f"Jen dough-bray {name}! Welcome to {self.cafe_name}!") # Jen dough-bray -> Dzien dobry -> Good day

    def run(self):
        self.getCustomer()

        #LOOP - 1) Order? 2) View Menu? 3) View Order History? 4) Leave?
        running = True
        while running:
            prompt = "Would you like to see the menu, see previous order history, order food, or exit"
            choice = self.getRequest(self.main_options, prompt)

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