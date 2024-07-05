from Orders import Order, OrderItem
from SPXCafe import SPXCafe

class Customer(SPXCafe):
    
    def __init__(self, username=None, customerId=None, firstname=None, lastname=None):
        '''Constructor Method:
        Arguments:
            - must be either username or customerId if existing
            - no customerId if new Customer requested
        '''
        super().__init__()
        self.__first_name = firstname
        self.__last_name = lastname
        if self.existsDB():
            self.setCustomer(username, customerId)
            self.setOrders()
    
    def getFirstName(self):
        return self.__first_name
    
    def getLastName(self):
        return self.__last_name
    
    def getUserName(self):
        return self.__username
    
    def getCustomerId(self):
        return self.__customer_id
    
    def setUserName(self, username):
        self.__user_name = username
    
    def existsDB(self):
        '''Check if object already exists in database '''
        retcode = False
        sql = None
        if self.getCustomerId():
            sql = f"SELECT count(*) AS count FROM customers WHERE cutomerId={self.getCustomerId()}"
        elif self.getUserName():
            sql = f"SELECT count(*) AS count FROM customers WHERE userName='{self.getUserName()}'"
        if sql:
            countData = self.dbGetData(sql)
            count = int(countData['count'])
            if count > 0:
                retcode = True
        return retcode
    
    def setCustomer(self, user_name=None, customerId=None):
        '''Creates Customer Object from database info
        Arguments: either user_name or customerId'''
        if user_name:
            self.__user_name = user_name
        if customerId:
            self.__customer_id = customerId
        customerData = None
        if self.getCustomerId(): # Customer must exist
            sql = f'''
            SELECT customerId, userName, firstName, lastName
            FROM customers
            WHERE customerId = {self.getCustomerId()}
            ORDER BY customerId
            '''
        elif self.getUserName():
            sql = f'''
            SELECT customerId, userName, firstName, lastName
            FROM customers
            WHERE userName = '{self.getUserName()}'
            ORDER BY customerId
            '''
        customerData = self.dbGetData(sql)

        if customerData:
            # Existing Customer - should only be ONE customer
            self.__customer_id = customerData[0]['customerId']
            self.__username = customerData[0]['userName']
            self.__first_name = customerData[0]['firstName']
            self.__last_name = customerData[0]['lastName']

    def saveNewCustomer(self) -> None:
        '''Inserts a new customer entry into the customer database. '''
        sql = f"""
            INSERT INTO customers
            (userName, firstName, lastName)
            VALUES
            ({self.__user_name}, {self.__first_name}, {self.__last_name})
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
        sql = f"""

        """
        