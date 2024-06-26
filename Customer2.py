# from Order import Order
# from OrderItem import Orderitem
from SPXCafe import SPXCafe

class Customer(SPXCafe):
    
    def __init__(self, username=None, customerId=None, firstname=None, lastname=None):
        '''Constructor Method:
        Arguments:
            - must be either username or customerId if existing
            - no customerId if new Customer requested
        '''
        super().__init__()

        self.setCustomer(username, customerId, firstname, lastname)
        # self.setOrders()

        if self.existsDB():
            self.setCustomer()
    
    def getFirstName(self):
        return self.__first_name
    
    def getLastName(self):
        return self.__last_name
    
    def getUserName(self):
        return self.__username
    
    def getCustomerId(self):
        return self.__customer_id
    
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
        Arugments: either user_name or customerId'''
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
            retcode = True
    
    @classmethod
    def findUser(cls, user_name=None):
        sql = f"""

        """
        