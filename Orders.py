from SPXCafe import SPXCafe
from Meal import Meal

class OrderItem(SPXCafe):
    '''Order Item Object for storing single meal type of an order. Order Id must be set before OrderItem can be saved. '''

    def __init__(self, mealId=None, quantity=None, orderItemId=None) -> None:
        super().__init__()
        self.setOrderItem(mealId, quantity, orderItemId)

    def setOrderItem(self, mealId, quantity, orderItemId) -> None:
        '''If orderItemId is given, retrieves data from database, otherwise sets new OrderItem instance. '''
        if orderItemId:
            self.__item_id = orderItemId
            sql = f"""
                SELECT orderId, mealId, quantity, mealPrice
                FROM orderItems
                WHERE orderItemId={self.__item_id}
                ORDER BY orderItemId
            """
            orderItemData = self.dbGetData(sql)
            if orderItemData:
                self.__order_id = orderItemData[0]['orderId']
                self.__meal_id = orderItemData[0]['mealId']
                self.__meal_name = Meal(mealId=self.__meal_id).get_meal_name()
                self.__meal_price = orderItemData[0]['mealPrice']
                self.__quantity = orderItemData[0]['quantity']
            else:
                print(f"OrderItem Database Error: no order item with id <{self.__item_id}>")
        else:
            if quantity < 1:
                print("OrderItem error: quantity must be greater than zero ")
            elif mealId:
                meal = Meal(mealId=mealId)
                if meal.exists_db():
                    self.__item_id = None
                    self.__meal_id = mealId
                    self.__meal_name = meal.get_meal_name()
                    self.__quantity = quantity  
                    self.__meal_price = meal.get_meal_price()
                else:
                    print('Menu Database Error: no meals with given id ')

    def setOrderId(self, orderId) -> None:
        self.__order_id = orderId

    def getItemId(self) -> int:
        return self.__item_id

    def getOrderId(self) -> int:
        return self.__order_id

    def getMealId(self) -> int:
        return self.__meal_id
    
    def getMealName(self) -> str:
        return self.__meal_name

    def getQuantity(self) -> int:
        return self.__quantity

    def getPrice(self) -> int:
        return self.__meal_price * self.__quantity
    
    def existsDB(self) -> bool:
        '''Checks if the order item exists by order item id. '''
        retcode = False
        if self.__item_id:
            sql = f"SELECT count(*) AS count FROM orderItems WHERE orderItemId={self.__item_id}"
            countData = self.dbGetData(sql)
            if countData:
                count = int(countData[0]['count'])
            if count > 0:
                retcode = True
        return retcode

    def save(self) -> None:
        '''If order id has been set: if order item already exists, updates information, otherwise creates new entry in database and sets order item id. '''
        try:
            self.__order_id
        except:
            print("Save Error: no order id given ")
        else:
            if self.existsDB():
                sql = f"""UPDATE orderItems SET
                    orderId={self.__order_id},
                    mealId={self.__meal_id},
                    quantity={self.__quantity},
                    mealPrice={self.__meal_price}
                    WHERE orderItemId={self.__item_id}
                """
                self.dbChangeData(sql)
            else:
                sql = f"""
                    INSERT INTO orderItems
                    (orderId, mealId, quantity, mealPrice)
                    VALUES
                    ({self.__order_id}, {self.__meal_id}, {self.__quantity}, {self.__meal_price})
                """
                self.__item_id = self.dbPutData(sql)

    @classmethod
    def getOrderItems(cls, orderId) -> list:
        '''Class Method: Returns a list of OrderItem objects with order id given. '''
        orderItems = []
        sql = f"""
            SELECT orderItemId
            FROM orderItems
            WHERE orderId={orderId}
            ORDER BY orderItemId
        """
        orderItemData = SPXCafe().dbGetData(sql)
        for orderItemRecord in orderItemData:
            orderItem = OrderItem(orderItemId=orderItemRecord['orderItemId'])
            orderItems.append(orderItem)
        return orderItems
    
    def display(self):
        print(f" - {str(self.__quantity):2s}x {self.__meal_name.title():20s} @ ${self.__meal_price:<5.2f} each")


class Order(SPXCafe):
    '''Order Object for storing a single order's information. '''

    def __init__(self, orderId=None, customerId=None) -> None:
        super().__init__()
        self.setOrder(orderId, customerId)

    def setOrder(self, orderId, customerId) -> None:
        '''If order id is given, retrieves data from database, otherwises sets new Order instance. '''
        if orderId:
            self.__order_id = orderId
            sql = f"""
                SELECT orderDate, customerId
                FROM orders
                WHERE orderId={self.__order_id}
            """
            orderData = self.dbGetData(sql)
            if orderData:
                self.__date = orderData[0]['orderDate']
                self.__customer_id = orderData[0]['customerId']
                self.__items = OrderItem.getOrderItems(self.__order_id)
            else:
                print(f"Order Database Error: no order with id <{self.__order_id}> ")
        else:
            self.__date = self.get_today()
            self.__customer_id = customerId
            self.__items: list[OrderItem] = []
            self.__order_id = None

    def getDate(self) -> str:
        return self.__date
    
    def getCustomerId(self) -> int:
        return self.__customer_id
    
    def getOrderId(self) -> int:
        return self.__order_id
    
    def getItems(self) -> list[OrderItem]:
        return self.__items
    
    def getTotalPrice(self) -> float:
        price = 0
        for item in self.__items:
            price += item.getPrice()
        return price
    
    def getTotalQuantity(self) -> int:
        quantity = 0
        for item in self.__items:
            quantity += item.getQuantity()
        return quantity
    
    def placeItem(self, mealId, quantity) -> None:
        self.__items.append(OrderItem(mealId, quantity))
    
    def existsDB(self) -> bool:
        '''Checks if the order already exists in the database by id. '''
        retcode = False
        if self.__order_id:
            sql = f"SELECT count(*) AS count FROM orders WHERE orderId={self.__order_id}"
            countData = self.dbGetData(sql)
            if countData:
                count = int(countData[0]['count'])
            if count > 0:
                retcode = True
        return retcode
    
    def save(self) -> None:
        '''If order already exists in the database, updates the date information, 
        otherwise inserts a new order to the database and sets the order id. '''
        if self.existsDB():
            sql = f"""UPDATE orders SET
                orderDate={self.__date},
                WHERE orderId={self.__order_id}
            """
            self.dbChangeData(sql)
            for item in self.__items:
                item.save()
        else:
            sql = f"""
                INSERT INTO orders
                (orderDate, customerId)
                VALUES
                ('{self.__date}', {self.__customer_id})
            """
            self.__order_id = self.dbPutData(sql)
            for item in self.__items:
                item.setOrderId(self.__order_id)
                item.save()

    def display(self):
        print(f"Order: <{self.__order_id}> {self.__date:>30}")
        for item in self.__items:
            item.display()
        print(f"Total Price: {' '*21} ${self.getTotalPrice():.2f}")


def main() -> None:
    ordritm1 = OrderItem(1, 3)
    ordritm2 = OrderItem(3, 2)
    ordritm3 = OrderItem(10, 1)

    ordr = Order()
    ordr.setOrder(2, None)

    ordr.display()

if __name__ == "__main__":
    main()