from SPXCafe import SPXCafe
import Course
from rapidfuzz.fuzz import partial_ratio #, QRatio, ratio, WRatio

class Meal(SPXCafe):
    
    def __init__(self, mealId=None, mealName=None, mealPrice=None, courseId=None, course=None) -> None:
        super().__init__()

        self.set_meal_id(mealId)
        self.set_meal_name(mealName)
        self.set_meal_price(mealPrice)
        self.set_course_id(courseId)
        self.set_course(course)

        # This checks if Meal already exists... if so, just load it.
        if self.exists_db():
            if not self.set_meal():
                print(f"Meal: Meal Id <{self.get_meal_id()}> is invalid ")
        else:
            self.save()

    def set_meal(self, mealId=None) -> bool:
        '''Set the Meal Attributes with values from Database for a mealId'''
        retcode = False
        if mealId:
            self.set_meal_id(mealId)

        if self.get_meal_id():
            sql = f"SELECT mealId, mealName, mealPrice, courseId FROM meals WHERE mealId = {self.get_meal_id()}"
            mealData = self.dbGetData(sql)
            for meal in mealData:
                self.set_meal_id(meal['mealId'])
                self.set_meal_name(meal['mealName'])
                self.set_meal_price(meal['mealPrice'])
                self.set_course_id(meal['courseId'])
                self.set_course()
            retcode = True
        return retcode
    
    # Getters/Setters of Attributes

    def set_meal_id(self, mealId=None) -> None:
        self.__mealId = mealId

    def set_meal_name(self, mealName=None) -> None:
        self.__mealName = mealName

    def set_meal_price(self, mealPrice=None) -> None:
        self.__mealPrice = mealPrice

    def set_course_id(self, courseId=None) -> None:
        self.__courseId = courseId

    def set_course(self, course=None) -> None:
        '''Save the owning Course for this Meal - bi-directional association'''
        if course:
            self.__course = course
            self.set_course_id(self.__course.get_course_id())
        else:
            if self.get_course_id():
                self.__course = Course.Course(courseId=self.get_course_id())
            else:
                self.__course = None

    def get_meal_id(self) -> int:
        return self.__mealId

    def get_meal_name(self) -> str:
        return self.__mealName
    
    def get_meal_price(self) -> float:
        return self.__mealPrice
    
    def get_course_id(self) -> int:
        return self.__courseId
    
    def get_course(self):
        return self.__course
    
    def __str__(self) -> str:
        '''Return a stringified version of object for print fucntions - may be same/different from display() method'''
        return f"Meal: <{self.get_course_id():2d}-{self.get_meal_id():2d}> {self.get_meal_name().title():20s} ${self.get_meal_price():5.2f}"
    
    def display(self) -> None:
        '''Formal display Meal'''
        print(f"Meal: <Course: {self.get_course_id():2d} {self.get_course().get_course_name().title()}, Meal: {self.get_meal_id():2d}> {self.get_meal_name().title():20s} ${self.get_meal_price():5.2f}")

    def exists_db(self):
        '''Check if object already exists in database'''
        retcode = False
        # Use Primary Key to check if the Meal exists in DB
        if self.get_meal_id():
            sql = f"SELECT count(*) AS count FROM meals WHERE mealId={self.get_meal_id()}"
            countData = self.dbGetData(sql)
            if countData:
                for countRecord in countData:
                    count = int(countRecord['count'])
                if count > 0:
                    retcode = True
        return retcode
    
    def save(self):
        '''Save meal data back to the database'''
        if self.get_course():
            self.set_course_id(self.get_course().get_course_id())

        if self.exists_db():
            sql = f'''UPDATE meals SET
                mealId={self.get_meal_id()}
                mealName={self.get_meal_name()}
                mealPrice={self.get_meal_price()}
                courseId={self.get_course_id()}
                WHERE mealId={self.get_meal_id()}
            '''
            self.dbChangeData(sql)
        else:
            sql = f'''
                INSERT INTO meals
                (mealName, mealPrice, courseId)
                VALUES
                ('{self.get_meal_name()}', {self.get_meal_price()}, {self.get_course_id()})
            '''
            # Save new primary key
            self.set_meal_id(self.dbPutData(sql))

    @classmethod
    def get_meals(cls, course):
        '''Class Method: Gets Meals for a Course object/instance - example of Aggregation'''
        sql = f"SELECT mealId, mealName, mealPrice, courseId FROM meals WHERE courseId={course.get_course_id()}"
        print(sql)
        mealsData = SPXCafe().dbGetData(sql)
        meals = []
        for mealData in mealsData:
            meal = cls.__new__(cls)
            meal.set_meal_id(mealData['mealId'])
            meal.set_meal_name(mealData['mealName'])
            meal.set_meal_price(mealData['mealPrice'])
            meal.set_course_id(mealData['courseId'])
            meal.set_course(course)
            meals.append(meal)
        return meals
    
    def find_meal(self, searchMeal=None):
        if searchMeal:
            if (True if partial_ratio(searchMeal, self.get_meal_name()) > 80 else False):
                return self

def main() -> None:
    meal = Meal(mealId=1)
    meal.display()
    # meal.set_meal_price(meal.get_meal_price()+1)
    # meal.save()
    # meal = Meal(mealId=1)
    # meal.display()

    # print("Creating NEW meal not in database...")
    # meal = Meal(mealName="Salata", mealPrice=3.45, courseId=1)
    # meal.display()
    # print(meal.find_meal("salata"))

if __name__ == "__main__":
    main()