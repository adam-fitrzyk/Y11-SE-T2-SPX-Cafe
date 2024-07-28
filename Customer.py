from Orders import Order, OrderItem
from SPXCafe import SPXCafe

class Customer(SPXCafe):
    
    def __init__(self, username=None, customerId=None, firstname=None, lastname=None):
        '''Constructor Method:
        Arguments:
            - must be either username or customerId if existing
            - no customerId if new Customer requested, username, first and last name required
        '''
        super().__init__()
        if firstname:
            firstname = firstname.lower()
        if lastname:
            lastname = lastname.lower()
        self.__first_name = firstname
        self.__last_name = lastname
        self.__user_name = username
        self.__customer_id = customerId
        if self.existsDB():
            self.setCustomer()
            self.setOrders()
        else:
            self.saveNewCustomer()
    
    def getFirstName(self):
        return self.__first_name
    
    def getLastName(self):
        return self.__last_name
    
    def getUserName(self):
        return self.__user_name
    
    def getCustomerId(self):
        return self.__customer_id

    def getName(self):
        return f"{self.__first_name.title()} {self.__last_name.title()}"
    
    def getOrders(self):
        return self.__orders
    
    def setUserName(self, username):
        self.__user_name = username
    
    def existsDB(self):
        '''Check if object already exists in database '''
        retcode = False
        sql = None
        if self.__customer_id:
            sql = f"SELECT count(*) AS count FROM customers WHERE customerId={self.__customer_id}"
        elif self.__user_name:
            sql = f"SELECT count(*) AS count FROM customers WHERE userName='{self.__user_name}'"
        if sql:
            countData = self.dbGetData(sql)
            if countData:
                count = int(countData[0]['count'])
                if count > 0:
                    retcode = True
        return retcode
    
    def setCustomer(self):
        '''Creates Customer Object from database info, for if customer already exists
        Arguments: either user_name or customerId'''
        customerData = None
        if self.getCustomerId(): # Customer must exist
            sql = f'''
            SELECT customerId, userName, firstName, lastName
            FROM customers
            WHERE customerId={self.getCustomerId()}
            ORDER BY customerId
            '''
        elif self.getUserName():
            sql = f'''
            SELECT customerId, userName, firstName, lastName
            FROM customers
            WHERE userName='{self.getUserName()}'
            ORDER BY customerId
            '''
        customerData = self.dbGetData(sql)

        if customerData:
            # Existing Customer - should only be ONE customer
            self.__customer_id = customerData[0]['customerId']
            self.__user_name = customerData[0]['userName']
            self.__first_name = customerData[0]['firstName']
            self.__last_name = customerData[0]['lastName']

    def saveNewCustomer(self) -> None:
        '''Inserts a new customer entry into the customer database. '''
        sql = f"""
            INSERT INTO customers
            (userName, firstName, lastName)
            VALUES
            ('{self.__user_name}', '{self.__first_name}', '{self.__last_name}')
        """
        self.__customer_id = self.dbPutData(sql)

    def setOrders(self) -> None:
        self.__orders = []
        if self.existsDB():
            sql = f"""
                SELECT orderId, orderDate
                FROM orders
                WHERE customerId={self.__customer_id}
                ORDER BY orderDate
            """
            orderData = self.dbGetData(sql)

            if orderData:
                for orderRecord in orderData:
                    order = Order(orderId=orderRecord['orderId'])
                    self.__orders.append(order)
    
    @classmethod
    def findUser(cls, user_name=None):
        '''Returns the customer id of the customer profile by username. '''
        customerId = None
        if user_name:
            sql = f"""
                SELECT customerId
                FROM customers
                WHERE userName='{user_name}'
            """
            customerData = SPXCafe().dbGetData(sql)
            if customerData:
                customerId = customerData[0]['customerId']
        return customerId
    
    def display(self):
        print(f"Customer: <{self.__customer_id}> {self.getName()}")

    def displayOrders(self):
        self.display()
        print()
        for order in self.__orders:
            order.display()
            print()
        

def main() -> None:
    c = Customer(username='adamiscool')
    c.displayOrders()

if __name__ == "__main__":
    main()