import sqlite3
from Database import Database
from Avatar import Avatar
from rapidfuzz import fuzz
from SPXCafe import SPXCafe

class MenuDB(Database):
    def __init__(self):
        dbname = r'C:\Users\FITR05\OneDrive - St Pius X College\Year 11\Software Engineering\VSCode\SPX_Cafe\SPX_Cafe.db'
        self.meals = None
        self.courses = None
        super().__init__(dbname)
    
    def get_courses(self) -> dict[str: int]:
        courses = {}
        sql = """
            SELECT 
                courseId, 
                courseName 
            FROM 
                courses 
            ORDER BY 
                courseId
        """
        coursesData = self.dbGetData(sql)
        if coursesData:
            for course in coursesData:
                courseName = course['courseName']
                courseId = course['courseId']
                courses[courseName] = courseId
            return courses
        else:
            print("No courses")
    
    def get_meals(self) -> dict[str: float]:
        meals = {}
        sql = """
            SELECT
                m.mealName,
                m.mealPrice
            FROM
                meals AS m
            ORDER BY
                m.mealName,
                m.mealPrice
        """
        mealsData = self.dbGetData(sql)
        if mealsData:
            for meal in mealsData:
                mealName = meal['mealName']
                mealPrice = meal['mealPrice']
                meals[mealName] = mealPrice
            return meals
        else:
            print("No meals")
    
    def show_meals_for_course(self, courseName: str = None) -> None:
        self.courses = self.get_courses()
        if courseName not in self.courses:
            print(f"Error: Course {courseName} does not exist")
        else:
            sql = f"""
                SELECT
                    m.mealName,
                    m.mealPrice
                FROM
                    courses AS c,
                    meals AS m
                WHERE
                    c.courseId = m.courseId
                AND
                    c.courseName = '{courseName}'
                ORDER BY
                    m.mealName,
                    m.mealPrice
            """
            mealsData = self.dbGetData(sql)
            if mealsData:
                for meal in mealsData:
                    print(f">>> {meal['mealName'].title():20s} ${meal['mealPrice']:.2f}")
            else:
                print(f"No meals for {courseName.title()} course")

    def get_meals_for_course(self, courseName: str = None) -> dict[str: float]:
        self.courses = self.get_courses()
        if courseName not in self.courses:
            print(f"Error: Course {courseName} does not exist")
        else:
            self.meals = {}
            sql = f"""
                SELECT
                    m.mealName,
                    m.mealPrice
                FROM
                    courses AS c,
                    meals AS m
                WHERE
                    c.courseId = m.courseId
                AND
                    c.courseName = '{courseName}'
                ORDER BY
                    m.mealName,
                    m.mealPrice
            """
            mealsData = self.dbGetData(sql)
            if mealsData:
                for meal in mealsData:
                    mealName = meal['mealName']
                    mealPrice = meal['mealPrice']
                    self.meals[mealName] = mealPrice
                return self.meals
            else:
                print(f"No meals for {courseName.title()} course")

    def insert_meal(self, mealName: str = None, mealPrice: float = None, courseName: str = None) -> int | None:
        self.courses = self.get_courses()
        self.meals = self.get_meals()
        newId = None
        if courseName not in self.courses:
            print(f"Error: Course {courseName} does not exist")
        elif mealName in self.meals:
            print(f"Meal {mealName} already exists")
        else:
            courseId = self.courses[courseName]
            sql = f"""
            INSERT INTO meals (
                mealName, mealPrice, courseId
                )
                VALUES ('{mealName}', {mealPrice}, {courseId})
            """
            newId = self.dbPutData(sql)
        return newId
    
    def delete_meal(self, mealName) -> int | None:
        self.meals = self.get_meals()
        mealId = None
        if mealName in self.meals:
            sql = f"""
                DELETE FROM meals
                WHERE
                    mealName = '{mealName.lower()}'
            """
            mealId = self.dbChangeData(sql)
            print("New meal ID", mealId)
        else:
            print(f"No meal named {mealName.title()}")
        return mealId

    def show_menu(self) -> None:
        self.courses = self.get_courses()
        print(f"{'-'*12}" + " MENU " + f"{'-'*12}")
        for courseName in self.courses:
            print(f"{'-'*6}" + f" Course: {courseName.title()} " + f"{'-'*6}")
            self.show_meals_for_course(courseName)
            print()

def extract_matches(choice, options):
    best_matches = []
    matches_ratios = []
    for option in options:
        ratio = fuzz.partial_ratio(choice, option)
        matches_ratios.append((option, ratio))
    best_ratio = max([item[1] for item in matches_ratios])
    print(matches_ratios)
    if best_ratio < 75:
        return None
    for item in matches_ratios:
        if item[1] == best_ratio:
            best_matches.append(item[0])
    return best_matches

def main() -> None:
    asking = True

    m = SPXCafe()
    m.show_menu()
    m.insert_meal('prawn cocktail', 5.40, 'entree')
    m.show_menu()
    m.delete_meal('prawn cocktail')
    m.show_menu()

    waiter = Avatar('luinda')
    waiter.say('Here are the courses.')
    courses_list = ', '.join([starter for starter in m.get_courses()])
    waiter.say(courses_list)

    while asking:
        choice = waiter.listen(f"Please choose a course: ", 5)
        matches = extract_matches(choice, m.get_courses())
        if not matches:
            waiter.say("Sorry, I didn't catch that, please tell me again.")
        else:
            waiter.say(f"You chose: {', '.join(matches)}")
            asking = False

if __name__ == "__main__":
    main()