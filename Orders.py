import SPXCafe

class OrderItem(SPXCafe.SPXCafe):
    '''Singular mealtype OrderItem Object. Order Id must be set before OrderItem can be saved. '''

    def __init__(self, mealId, quantity) -> None:
        super().__init__()
        self.setOrderItem(mealId, quantity)

    def setOrderItem(self, mealId, quantity) -> None:
        if quantity < 1:
            print("OrderItem error: quantity must be greater than zero ")
        elif mealId:
            sql = f"SELECT count(*) AS count FROM meals WHERE mealId={mealId}"
            countData = self.dbGetData(sql)
            if countData:
                count = int(countData['count'])
                if count > 0: 
                    self.__item_id = None
                    self.__meal_id = mealId 
                    self.__quantity = quantity   
                    sql = f"SELECT mealPrice FROM meals WHERE mealId={mealId}"
                    priceData = self.dbGetData(sql)
                    self.__meal_price = priceData['mealPrice']
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

    def getQuantity(self) -> int:
        return self.__quantity

    def getPrice(self) -> int:
        return self.__meal_price * self.__quantity
    
    def existsDB(self) -> bool:
        retcode = False
        if self.__item_id:
            sql = f"SELECT count(*) AS count FROM orderItems WHERE orderItemId={self.__item_id}"
            countData = self.dbGetData(sql)
            if countData:
                count = int(countData['count'])
            if count > 0:
                retcode = True
        return retcode

    def save(self) -> None:
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


class Order(SPXCafe.SPXCafe):
    '''Order Object for storing a single order's information. '''

    def __init__(self, customerId) -> None:
        super().__init__()
        self.setOrder(customerId)

    def setOrder(self, customerId) -> None:
        '''Sets the date to today, sets customer id, and sets order id to None. '''
        self.__order_id = None
        self.__items: list[OrderItem] = []
        self.__date = self.get_today()
        self.__customer_id = customerId

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
        '''Checks if the order id already exists in the database. '''
        retcode = False
        if self.__order_id:
            sql = f"SELECT count(*) AS count FROM orders WHERE orderId={self.__order_id}"
            countData = self.dbGetData(sql)
            if countData:
                count = int(countData['count'])
            if count > 0:
                retcode = True
        return retcode
    
    def save(self) -> None:
        '''If order already exists in the database, updates the date information, otherwise inserts a new order to the database and sets the order id. '''
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
                ({self.__date}, {self.__customer_id})
            """
            self.__order_id = self.dbPutData(sql)
            for item in self.__items:
                item.setOrderId(self.__order_id)
                item.save()


def main() -> None:
    pass

if __name__ == "__main__":
    main()