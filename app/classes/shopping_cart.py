# Tanner

class ShoppingCart():
    def __init__(self, user):
        self.user = user
        self.number_of_items = 0
        self.items = []
        self.total_cost = 0
        


    def display_cart(self):
        pass


    def remove(self, index, quantity, db) -> bool:
        if index > len(self.items) - 1:   # Protect against out of index
            print("Error! Only valid options please!!")
        if self.items[index].quantity - quantity < 0:   # Protect against removing more books than exist
            quantity = self.items[index].quantity
        self.items[index].quantity -= quantity
        cur = db.cursor()
        try:
            if self.items[index].quantity == 0:
                removed_book = self.items.pop(index)
                sql = 'DELETE FROM Cart WHERE ISBN=? AND username=?'
                cur.execute(sql, (removed_book.ISBN, self.user.username))
                db.commit()
                self.refresh_price()
                return True
            elif self.items[index].quantity > 0:
                sql = 'UPDATE Cart SET quantity=? WHERE ISBN=? AND username=?'
                values = (self.items[index].quantity, self.items[index].ISBN, self.user.username)
                cur.execute(sql, values)
                db.commit()
                self.refresh_price()
                return True
        except:
            print('Unkown error occured.')
            return False


    def add(self, book, quantity, db) -> bool:
        # First, ensure that there are enough books in stock to supply the cart.
        cur = db.cursor()
        sql = 'SELECT quantity FROM Books WHERE ISBN=?'
        values = (book.ISBN,)
        cur.execute(sql, values)
        qty_in_db = cur.fetchone()[0]
        if qty_in_db < quantity:
            print("Error, you can't add more than are in stock!")
            self.refresh_price()
            return False

        for item in self.items:     # If item already in cart, process accordingly.
            if item.ISBN == book.ISBN:
                if qty_in_db < quantity + item.quantity:
                    print("Error, you can't add more than are in stock!")   # Once again, protecting from adding too much qty
                    self.refresh_price()
                    return False
                item.quantity += quantity
                sql = 'UPDATE Cart SET quantity=? WHERE ISBN=? AND USERNAME=?'
                new_values = (item.quantity, item.ISBN, self.user.username)
                cur.execute(sql, new_values)
                db.commit()
                self.refresh_price()
                return True
        
        # If no item exists in the cart table and cart list, add it.
        self.items.append(book)
        sql = ''' INSERT INTO Cart(ISBN,username,quantity)
            VALUES(?,?,?) '''
        new_values = (book.ISBN, self.user.username, book.ISBN)
        cur.execute(sql, new_values)
        db.commit()
        self.refresh_price()
        return True
        


    #  Completely empty the cart list/table (where entries are under the current user's username)
    def empty(self, db) -> None:
        cur = db.cursor()
        sql = 'DELETE FROM Cart WHERE username=?'
        cur.execute(sql, (self.user.username,))
        db.commit()
        self.items.clear()



    def checkout(self, db) -> None:
        cur = db.cursor()
        for item in self.items:
            sql = 'SELECT quantity FROM Cart WHERE ISBN=? AND username=?'
            values = (item.ISBN, self.user.username)
            cur.execute(sql, values)
            qty = cur.fetchone()[0]
            if qty < item.quantity:
                print("Error! More "+ item.title+" copies in cart than in stock! \n Please correct this and then try to checkout again.")
                return False
            
        

            



    def refresh_price(self) -> None:
        price = 0
        for item in self.items:
            price += (item.price * item.quantity)
        self.total_cost = price