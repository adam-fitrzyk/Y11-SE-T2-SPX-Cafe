from Database import Database
# from Orders import Orders

class Customer(Database):
    def __init__(self, dbname, userName=None) -> None:
        self.customerId = None
        self.userName   = None
        self.firstName  = None
        self.lastName   = None
        self.orders     = []

        if dbname:
            self.dbname = dbname
            super().__init__(dbname)
            if userName:
                if not self.setCustomer(userName):
                    print(f"Customer: Invalid Username provided - {userName}")
        else:
            print(f"Customer: Database invalid: {dbname}")

    # ----- Set up customer object data ----- #

    def setCustomer(self, userName=None) -> bool:
        retcode = False
        if userName:
            sql = f"""
                SELECT customerId, userName, firstName, lastName
                FROM customer
                WHERE userName = '{userName}'
                ORDER BY customerId
            """
            customerData = self.dbGetData(sql)

            if customerData:
                for customer in customerData:
                    self.customerId = customer['customerId']
                    self.userName   = customer['userName']
                    self.firstName  = customer['firstName']
                    self.lastName   = customer['lastName']
                    retcode = True
            else:
                self.customerId = None
                self.userName   = None
                self.firstName  = None
                self.lastName   = None
                print(f"Customer: '{userName}' not found")

        return retcode
    
    # ----- Get customer data ----- #

    def getCustomerName(self) -> str:
        if self.customerId:
            return f"{self.firstName} {self.lastName}"

    def getCustomerId(self) -> int:
        return self.customerId
    
    # ----- Formatted displays ----- #
    
    def displayCustomer(self) -> None:
        print(f"Customer: ({self.customerId}) - {self.getCustomerName()} <{self.userName}>")

def main() -> None:
    bloggs = Customer("SPX_Cafe.db", "bloggs")
    bloggs.displayCustomer()

if __name__ == "__main__":
    main()