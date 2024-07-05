from Database import Database
from datetime import datetime

class SPXCafe(Database):
    '''Wrapper Class around Database specific for SPXCafe Database'''

    def __init__(self) -> None:
        '''Constructor Method - defaults SPXCafe database'''
        self.__dbname = "SPX_Cafe.db"
        super().__init__(self.__dbname)

    # Assorted Utility Methods for ALL child classes ------------------
    
    def get_today(self) -> str:
        return datetime.today().date().strftime('%Y-%m-%d') # ISO format for dates - how sqlite and mysql store dates
    

def main() -> None:
    s = SPXCafe()
    print(s.get_today())

if __name__ == "__main__":
    main()