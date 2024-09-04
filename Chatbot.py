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

        # Create language interpretation dictionaries (maps) for decoding user inputs

        self.exit_keywords = ["exit", "leave", "quit"]
        self.order_keywords = ["order", "buy", "pay"]
        self.menu_keywords = ["menu"]
        self.history_keywords = ["order history", "previous", "past"]
        self.mainLine_lanMap = {
            "see menu":     self.menu_keywords,
            "order":    self.order_keywords,
            "see history":  self.history_keywords,
            "exit":     self.exit_keywords
        }
        self.polarQ_lanMap = {
            True:   ["yes", "yeah", "okay", "alright", "sure"],
            False:  ["no", "nope", "n't", "not"]
        }
        self.course_lanMap = self.createCourseLanguageMap()
        self.meal_lanMap = self.createMealLanguageMap()      
    
    # Language map constructors -----------------------------------------------------------------

    def createCourseLanguageMap(self) -> dict:
        ''''''
        courses = [course.get_course_name() for course in self.__menu.get_courses()]
        course_lanMap = {}
        for course in courses:
            course_lanMap[course] = [course]
        course_lanMap["checkout"] = ['complete', 'submit', 'finish', 'checkout']
        course_lanMap["abandon"]  = ["abandon", "exit", "leave", "go back"]
        return course_lanMap
    
    def createMealLanguageMap(self) -> dict:
        ''''''
        meal_lanMap = {}
        for course in self.__menu.get_courses():
            course_meal_options = {}
            for meal in course.get_meals():
                course_meal_options[meal.get_meal_name()] = [meal.get_meal_name()]
            course_meal_options["back"]     = ["go back", "nevermind", "see courses"]
            course_meal_options["checkout"] = ['complete', 'submit', 'finish', 'checkout']
            course_meal_options["abandon"]  = ["abandon", "exit", "leave"]
            meal_lanMap[course.get_course_name()] = course_meal_options
        return meal_lanMap

    # Core natural language processing methods ------------------------------------------------------------------------------------------

    def matchOptions(self, choice:str, lanMap:dict) -> str | None:
        '''Choose best match from avaliable options provided in language map, and return None unless only one option is matched. '''
        retlist = set()
        matches = []
        max_confidence = 0
        keywords = []
        items = [lanMap[option] for option in lanMap]
        for item in items:
            keywords += item

        results = extract(choice, keywords, processor=default_process)
        for result in results:
            (match, confidence, index) = result
            # print(f"Checking: {result}")
            if confidence > max_confidence and confidence > 80:
                max_confidence = confidence
                matches = [match]
            elif confidence == max_confidence:
                matches.append(match)

        # print(f"You have matched: {', '.join(matches)} with confidence level {max_confidence}%")

        for match in matches:
            for option in lanMap:
                if match in lanMap[option]:
                    retlist.add(option)

        if len(retlist) > 1:
            self.__waiter.say(f"Did you mean {', or '.join(retlist)}? Please try again.")
        elif len(retlist) == 0:
            self.__waiter.say("Sorry I did not understand that, please try again.")
        elif retlist:
            return list(retlist)[0]

    def getRequest(self, lanMap, prompt) -> str:
        '''Keep asking the customer to choose an option until they choose just one. '''
        response = None
        self.__waiter.say(f"Alright {self.__customer.getFirstName()}. {prompt}?")
        while response == None:
            print(f"> {prompt}?")
            option = self.__waiter.listen('', use_sr, phrase_time_limit)
            response = self.matchOptions(option, lanMap)
        self.__waiter.say(f"You chose: {response}")
        return response
    
    # Login and registration methods ----------------------------------------------------------------------------------------------------------
    
    def getCustomer(self) -> None:
        '''Get a customer - using username typed in for accuracy, otherwise create a new customer account. '''
        # Ask if customer already has an account or needs to create a new one
        prompt = "Are you an existing customer?"
        existing_customer = None
        while existing_customer == None:
            speech = self.__waiter.listen(prompt, use_sr, phrase_time_limit)
            existing_customer = self.matchOptions(speech, self.polarQ_lanMap)
        
        if existing_customer:
            # Look up customer and welcome back
            customer_id = None
            while customer_id == None:
                username = self.__waiter.listen("Please enter your username", use_sr=False)
                print("... Checking our customer database ...")
                customer_id = Customer.findUser(username)
                if customer_id:
                    self.__customer = Customer(customerId=customer_id)
                    self.welcomeCustomer(self.__customer.getName())
                else:
                    self.__waiter.say(f"I'm sorry, I couldn't find {username} in our database.")
        else:
            # Ask customer for username, first name and last name and create new customer account
            self.welcomeCustomer()
            username = self.__waiter.listen("Please enter your username", use_sr=False)
            first_name = None
            last_name = None
            while not first_name:
                inp_name = self.__waiter.listen("Please tell me your first name?", use_sr, phrase_time_limit)
                first_name = self.__nlp.getNamesByPartsOfSpeech(inp_name)
            while not last_name:
                inp_name = self.__waiter.listen("Please tell me your last name?", use_sr, phrase_time_limit)
                last_name = self.__nlp.getNamesByPartsOfSpeech(inp_name)
            self.__customer = Customer(username=username, firstname=first_name, lastname=last_name)

    def welcomeCustomer(self, name='') -> None:
        self.__waiter.say(f"Jen dough-bray {name}! Welcome to {self.cafe_name}!") # Jen dough-bray -> Dzien dobry -> Good day

    # Cafe system methods ---------------------------------------------------------------------------------------------------------------

    def displayOrderHistory(self):
        self.__waiter.say(f"Ok, {self.__customer.getFirstName()}. Let's show you your previous orders.")
        print('-'*5 + "Order History" + '-'*5)
        self.__customer.displayOrders()

    def displayMenu(self):
        self.__waiter.say(f"Alright, {self.__customer.getFirstName()}. Let's show you the menu.")
        self.__menu.display()

        asking = True
        while asking:
            prompt = "Would you like me to describe any courses for you"
            see_descriptions = self.getRequest(self.polarQ_lanMap, prompt)
            if see_descriptions:
                prompt = "Which course would you like a description of"
                course_enquired = self.getRequest(self.course_lanMap, prompt)
                match course_enquired:
                    case "entree":
                        self.__waiter.say("This course contains light snacks to awaken your appetite!")
                    case "starter":
                        self.__waiter.say("This course contains small meals to fill up before the main dish. I would suggest getting only one or two of these dishes.")
                    case "main":
                        self.__waiter.say("This course contains our famous dishes to crush your hunger! I suggest only one of these per person.")
                    case "dessert":
                        self.__waiter.say("This course contains sugary snacks after your main meal to end the night on a sweet-note!")
            else:
                asking = False

    def orderFood(self):
        ''''''
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
                asking = True
                while asking:
                    course_choice = self.askCourse()
                    if course_choice == 'ABANDON':
                        asking_course, asking_meal, valid_order, asking = False, False, False, False
                    elif course_choice == 'CHECKOUT':
                        if order.getTotalQuantity() < 3:
                            self.__waiter.say(f"I'm sorry, but you cannot checkout unless you have ordered at least three items.")
                        else:
                            asking_course, asking_meal, asking = False, False, False
                    elif course_choice:
                        asking = False
                
                # Ask what meal customer wants to order, add to the order
                while asking_meal:
                    asking = True
                    while asking:
                        course_choice.display()
                        meal_choice, quantity = self.askMeal(course_choice)
                        if meal_choice == 'ABANDON':
                            asking_course, valid_order, asking = False, False, False
                        elif meal_choice == 'CHECKOUT':
                            if order.getTotalQuantity() < 3:
                                self.__waiter.say(f"I'm sorry, but you cannot checkout unless you have ordered at least three items.")
                            else:
                                asking_course, asking = False, False
                        elif meal_choice == 'BACK':
                            asking = False
                        elif meal_choice:
                            asking = False
                    if meal_choice in ['ABANDON', 'CHECKOUT', 'BACK']:
                        break

                    print(meal_choice, quantity)
                    self.__waiter.say(f"You chose to order {self.meal_lanMap[course_choice.get_course_name()][meal_choice.get_meal_name()]} {quantity} times.")

                    order.placeItem(meal_choice.get_meal_id(), quantity)

                    # Ask if customer wants to order another meal
                    prompt = "Would you like to order another meal"
                    order_another_meal = self.getRequest(self.polarQ_lanMap, prompt)
                    if not order_another_meal:
                        asking_meal = False

            print('-'*5 + 'Basket' + '-'*5)
            order.display()
            if valid_order:
                prompt = "Are you sure you would like to checkout"
                checkout = self.getRequest(self.polarQ_lanMap, prompt)
                if checkout:
                    order.save()
                    self.__customer.addOrder(order)

            prompt = "Would you like to make another order"
            order_again = self.getRequest(self.polarQ_lanMap, prompt)
            if not order_again:
                ordering = False

    def askCourse(self):
        ''''''
        self.__menu.display_courses()
        prompt = "Which course would you like to order from? Otherwise you can abandon or checkout"
        choice = self.getRequest(self.course_lanMap, prompt)
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
                speech = self.__waiter.listen(f"Which meal would you like to order? Otherwise you can abandon or checkout?", use_sr, phrase_time_limit)
                choice = self.matchOptions(speech, self.meal_lanMap[course.get_course_name()])
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
                    speech = self.__waiter.listen(f"How many of the {meal.get_meal_name()} would you like?", use_sr, phrase_time_limit)
                    number = self.__nlp.getNumbersByPartsOfSpeech(speech)
            if meal:
                prompt = f"Are you sure you would like to order {meal.get_meal_name()}"
                confirmed = self.getRequest(self.polarQ_lanMap, prompt)
                if not confirmed:
                    choice = None
        quantity = american_number_system[number[0]]
        return meal, quantity
    
    # Main method ---------------------------------------------------------------------------------------

    def run(self):
        ''''''
        print(self.__waiter.name)
        self.getCustomer()

        #LOOP - 1) Order? 2) View Menu? 3) View Order History? 4) Leave?
        running = True
        while running:
            prompt = "Would you like to see the menu, see previous order history, order food, or exit"
            choice = self.getRequest(self.mainLine_lanMap, prompt)

            if choice == "exit":
                self.__waiter.say(f"Thank you, {self.__customer.getFirstName()}, for ordering with {self.cafe_name}-bot today! Doh-vee-jeh-nia.")
                running = False
            elif choice == "see history":
                self.displayOrderHistory()
                input("Enter anything to go back: ")
            elif choice == "see menu":
                self.displayMenu()
                input("Enter anything to go back: ")
            elif choice == "order":
                self.orderFood()
                input("Enter anything to go back: ")


def main():
    polabot = Chatbot("Pola-bot", "Polander Plates", "Polander Plains")

    polabot.run()

if __name__ == "__main__":
    main()