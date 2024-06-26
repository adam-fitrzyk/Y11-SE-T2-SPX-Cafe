import Meal
from SPXCafe import SPXCafe
from rapidfuzz.fuzz import partial_ratio

class Course(SPXCafe):
    '''Course Class - holds information about a Menu Course '''

    def __init__(self, courseId=None, courseName=None, meals=None) -> None:
        '''Constructor Method for a Course'''
        super().__init__()
        self.set_course_id(courseId)
        self.set_course_name(courseName)
        self.set_meals(meals)

        # set the Meals Aggregations for this Course
        if self.exists_db():
            if not self.set_course():
                print(f"Course: Course Id <{self.get_course_id()}> is invalid ")

    def set_course(self, courseId=None) -> None:
        '''Retrieve course data from database'''
        retcode = False
        if courseId:
            self.set_course_id(courseId)
        
        if self.get_course_id():
            sql = f"SELECT courseId, courseName FROM courses WHERE courseId={self.get_course_id()}"
            print(sql)
            courseData = self.dbGetData(sql)

            if courseData: # Course found in database
                for course in courseData: # Retrieve data
                    self.set_course_id(course['courseId'])
                    self.set_course_name(course['courseName'])
                    self.set_meals(Meal.Meal.get_meals(self))
                    retcode = True
        return retcode

    # Getters / Setters for the class
    def set_course_id(self, courseId):
        self.__courseId = courseId

    def set_course_name(self, courseName=None):
        if courseName:
            self.__courseName = courseName.lower()
        else:
            self.__courseName = courseName

    def set_meals(self, meals=None):
        if meals:
            self.__meals = meals
        else:
            self.__meals = []

    def add_meal(self, meal=None):
        print(type(meal))
        if meal:
            self.__meals.append(meal)
            meal.set_course(self)

    def get_course_id(self):
        return self.__courseId
    
    def get_course_name(self):
        return self.__courseName
    
    def get_meals(self):
        return self.__meals
    
    def find_meal(self, searchMeal) -> list:
        meals = []
        if searchMeal:
            for meal in self.get_meals():
                retmeal = meal.find_meal(searchMeal)
                if retmeal:
                    meals.append(retmeal)
        return meals
    
    def find_course(self, searchCourse=None):
        if searchCourse:
            if (True if partial_ratio(searchCourse, self.get_course_name()) > 80 else False):
                return self
    
    def __str__(self) -> str:
        '''Return a stringified version of object for printing'''
        return f"Course <{self.get_course_id()}> {self.get_course_name().title() if self.get_course_name() else "<Unknown>"}"
    
    def display(self) -> None:
        '''Print the course details'''
        print(self)
        for meal in self.get_meals():
            print(' -', meal.display())

    # Persistent Data - Database - Related Methods
    def exists_db(self) -> bool:
        '''Check if object already exists in database'''
        retcode = False
        if self.get_course_id():
            sql = f"SELECT count(*) AS count FROM courses WHERE courseId={self.get_course_id()}"
            countData = self.dbGetData(sql)
            if countData:
                for entry in countData:
                    count = int(entry['count'])
                if count > 0:
                    retcode = True
        return retcode
    
    def save(self) -> None:
        '''Save course data back to the database'''
        if self.exists_db():
            sql = f"""UPDATE courses SET
                courseId={self.get_course_id()},
                courseName='{self.get_course_name()}'
                WHERE courseId={self.get_course_id()}
            """
            self.dbChangeData(sql)
        else:
            sql = f"""INSERT INTO courses
                (courseName)
                VALUES
                ('{self.get_course_name()}')
            """
            # Save new primary key
            self.set_course_id(self.dbPutData(sql))

    def delete(self):
        '''Deletes an Instance of a Course from the database only if there are no children MEALS'''
        if len(self.get_meals()) == 0:
            sql = f"DELETE FROM courses WHERE courseId={self.get_course_id()}"
            self.dbChangeData(sql)
        else:
            print(f"Cannot delete Course <{self.get_course_id()}> {self.get_course_name().title()} - Meals attached")

    @classmethod
    def get_courses(cls) -> list:
        '''Class Method: Gets all Courses object/instances for Menu - example of Aggregation'''
        sql = "SELECT courseId, courseName FROM courses ORDER BY courseId"
        coursesData = SPXCafe().dbGetData(sql)
        courses = []
        for courseData in coursesData:
            # Create a new instance
            course = cls.__new__(cls)
            course.set_course_id(courseData['courseId'])
            course.set_course_name(courseData['courseName'])
            course.set_meals(Meal.Meal.get_meals(course))
            # Add course object to courses list
            courses.append(course)
        return courses
    
def main() -> None:
    '''Test Harness to make sure all methods work'''

    course = Course(1)
    course.display()
    course.set_course_name(course.get_course_name()+"X")
    course.save()
    course = Course(1)
    course.display()

    course1 = Course(courseName="New Course")
    course1.save()
    course1.display()

    print("New Meal")
    meal = Meal.Meal(mealName="New Meal", mealPrice=99.99, course=course1)
    meal.display()
    print(course1.get_meals())

    course1.delete()

    course = Course()
    course.set_course(1)
    course.display()

if __name__ == "__main__":
    main()