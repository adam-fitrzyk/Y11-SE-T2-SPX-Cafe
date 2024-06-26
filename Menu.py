from Course import Course
from Meal import Meal
from SPXCafe import SPXCafe

class Menu(SPXCafe):

    def __init__(self, menuName=None) -> None:
        '''Constructor Method for the Menu '''
        super().__init__()
        self.set_menu_name(menuName)
        # Set the Menu to database values
        self.set_menu()

    # Getters / Setters for the Menu ----------------------------------------

    def set_menu(self) -> None:
        '''Setup Menu from database '''
        # Add Course Aggregations for this Menu - i.e. a list of Courses
        self.set_courses(Course().get_courses())

    def set_menu_name(self, menuName=None) -> None:
        '''Set the Menu Name - or default to "The Menu" '''
        if menuName:
            self.__menuName = menuName
        else:
            self.__menuName = "The Menu"

    def set_courses(self, courses=None) -> None:
        '''Set courses aggregation to list of courses or empty list '''
        if courses:
            self.__courses = courses
        else:
            self.__courses = []

    def get_menu_name(self) -> str:
        return self.__menuName

    def get_courses(self) -> list:
        return self.__courses
    
    # Output related methods -------------------------------------------
    
    def __str__(self) -> str:
        '''Returns a string for the Menu object for printing '''
        return f"Menu: {self.get_menu_name()}"
    
    def display(self) -> None:
        '''Display this Menu instance more formally '''
        print(f"{'-'*25} {self.get_menu_name()} {'-'*25}\n")

        if self.get_courses():
            for course in self.get_courses():
                course.display()

    def display_courses(self) -> None:
        '''Display all the Courses in a comma-seperated string '''
        print(f"Course List: ", end="")
        courseNames = []
        for course in self.get_courses():
            courseNames.append(course.get_course_name().title())
        print(", ".join(courseNames))

    # Adhoc Methods for Menu and aggregated Courses ----------------

    def find_meal(self, searchMeal=None) -> list[list]:
        '''Search through courses in menu for name of meal '''
        meals = []
        if searchMeal:
            for course in self.get_courses():
                retmeal = course.find_meal(searchMeal)
                if retmeal:
                    meals.append(retmeal)
        return meals

    def find_course(self, searchCourse=None):
        courses = []
        if searchCourse:
            for course in self.get_courses():
                    retcourse = course.find_course(searchCourse)
                    if retcourse:
                        courses.append(retcourse)
        return courses
    
def main():
    m = Menu("Ristorante Italia")
    m.display()
    m.display_courses()
    print('Searching for Course: <entree> ->', m.find_course('entree'))
    print('Searching for Meal: <pumpkin soup> ->', m.find_meal('pumpkin soup'))
    
if __name__ == "__main__":
    main()