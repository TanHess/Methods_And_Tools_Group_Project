# Tanner
from datetime import date
from .book import Book
from copy import deepcopy

class ShoppingCart():
    def __init__(self, user):
        self.user = user
        self.number_of_items = 0
        self.items = []
        self.total_cost = 0

    
    # Use this to initialize cart instead of __init__ 
    # This way, anonomous users can still have a cart object.
    def get_cart(self, db):
        self.items.clear()      # Empty the clientside cart to avoid calling this function multiple times and flooding the cart.
        cur = db.cursor()
        sql = 'SELECT ISBN, quantity FROM CART WHERE username=?'
        username_tuple = (self.user.username,)
        cur.execute(sql, username_tuple)
        isbns_quantity = cur.fetchall()     # Tuples holding isbns[0] and quantity[1]
        for isbn_qty in isbns_quantity:   # For loop adds all the books in the Users db Cart to their client side cart
            sql = 'SELECT * FROM BOOKS WHERE ISBN=?'
            isbn_tuple = (isbn_qty[0],)     # For fetching all the book information from the Books table
            cur.execute(sql, isbn_tuple)
            book = cur.fetchone()
            book_to_add = Book()
            book_to_add.ISBN = book[0]
            book_to_add.title = book[1]
            book_to_add.author = book[2]
            book_to_add.genre = book[3]
            book_to_add.format = book[4]
            book_to_add.price = float(book[5])
            book_to_add.quantity = int(isbn_qty[1]) # Use the Cart quantity, not the Books quantity
            self.items.append(book_to_add)
        self.refresh_price()    # Set total price of the cart



    # Function to refresh self.total_cost to the accurate cost of all of the items.
    def refresh_price(self) -> None:
        price = 0
        for item in self.items:
            price += (item.price * item.quantity)
        self.total_cost = price



    # In the real world, much more verification would take place but this is fake payment info anyways.
    def verify_payment_info(self, db) -> bool:
        cur = db.cursor()
        sql = 'SELECT cc FROM USERS WHERE username=?'
        user_tuple=(self.user.username,)
        cur.execute(sql,user_tuple)
        cc = int(cur.fetchone()[0])
        if self.user.payment_info.get('cc') != cc:
            return False            # Unverified cc info
        sql = 'SELECT cc_cvv FROM USERS WHERE username=?'
        cur.execute(sql,user_tuple)
        cc_cvv = int(cur.fetchone()[0])
        if self.user.payment_info.get('cc_cvv') != cc_cvv:
            return False            # Unverified cc_cvv info
        return True                 # User payment info verified, return true



    def display_cart(self):
        if len(self.items) == 0:
            print("No items to display, your cart is empty!")
            return
        for item in self.items:
            print('\n1)')
            print(item.__repr__())


    # Remove a book from the client and the database 
    def remove(self, index, quantity, db) -> bool:
        if index > len(self.items) - 1:   # Protect against out of index
            print("Error! Only valid options please!!")
            return False
        if self.items[index].quantity - quantity < 0:   # Protect against removing more books than exist
            quantity = self.items[index].quantity
        self.items[index].quantity -= quantity
        cur = db.cursor()
        try:
            if self.items[index].quantity == 0:
                removed_book = self.items.pop(index)
                sql = 'DELETE FROM CART WHERE ISBN=? AND username=?'
                cur.execute(sql, (removed_book.ISBN, self.user.username))
                db.commit()
                self.refresh_price()
                return True
            elif self.items[index].quantity > 0:
                sql = 'UPDATE CART SET quantity=? WHERE ISBN=? AND username=?'
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
        book_to_add = deepcopy(book)    # Prevent changing the original objects quantity by creating a new book object
        book_to_add.quantity = quantity
        cur = db.cursor()
        sql = 'SELECT quantity FROM BOOKS WHERE ISBN=?'
        values = (book_to_add.ISBN,)
        cur.execute(sql, values)
        qty_in_db = cur.fetchone()[0]
        if qty_in_db < quantity:
            print("Error, you can't add more than are in stock!")
            self.refresh_price()
            return False

        for item in self.items:     # If item already in cart, process accordingly.
            if item.ISBN == book_to_add.ISBN:
                if qty_in_db < quantity + item.quantity:
                    print("Error, you can't add more than are in stock!")   # Once again, protecting from adding too much qty
                    self.refresh_price()
                    return False
                item.quantity += quantity   # If we didn't return yet, then the user is adding more of this item to their cart
                sql = 'UPDATE CART SET quantity=? WHERE ISBN=? AND USERNAME=?'
                new_values = (item.quantity, item.ISBN, self.user.username)
                cur.execute(sql, new_values)
                db.commit()
                self.refresh_price()
                return True
        
        # If no item exists in the cart table and cart list, add it.
        self.items.append(book_to_add)
        sql = ''' INSERT INTO CART(ISBN,username,quantity)
            VALUES(?,?,?) '''
        new_values = (book_to_add.ISBN, self.user.username, book_to_add.quantity)
        cur.execute(sql, new_values)
        db.commit()
        self.refresh_price()
        return True
        


    #  Completely empty the cart list/table (where entries are under the current user's username)
    def empty(self, db) -> None:
        cur = db.cursor()
        sql = 'DELETE FROM CART WHERE username=?'
        cur.execute(sql, (self.user.username,))
        db.commit()
        self.items.clear()




    def checkout(self, db, verify=False) -> None:
        self.get_cart(db)         # Re-gathers the local cart to ensure that there is no discontinuity between the client cart and the db cart
        self.refresh_price()   # Ensure self.total_cost is up to date. 
        cur = db.cursor()
        if verify==True:    # Only call when user wants to use pre-existing payment info
            if self.verify_payment_info() == False:     # Ensure User payment info is valid.
                print("Error, payment info invalid.")   
                return False
        for item in self.items:     # First for loop checks all items have enough stock to checkout.
            sql = 'SELECT quantity FROM BOOKS WHERE ISBN=?'
            values = (item.ISBN,)
            cur.execute(sql, values)
            qty = cur.fetchone()[0]
            if qty < item.quantity:     # Check to ensure enough items of each book in stock before puchasing.
                print("Error! More '"+ item.title+"' copies in cart than in stock! \n Please correct this and then try to checkout again.")
                return False
        
        # Find the max order_number associated with the current users names and increments it by 1 (new order number)
        sql = 'SELECT MAX(order_number) FROM ORDERS WHERE username=?'
        username_tuple = (self.user.username,)
        cur.execute(sql,username_tuple)
        max = cur.fetchone()[0]
        if max == None:     # Protect against an error where no orders exist for the current user in the orders table.
            max = 0         
        max += 1            # New order_number to assign to all items going into the order table from this order.
        dt = date.today().strftime("%B %d, %Y")     # Current date (formatted) to put into the Orders table.
        for item in self.items:     # Next for loop adds each item to the orders table 
            sql = 'INSERT INTO ORDERS(username, title, date, ISBN, quantity, order_number) VALUES(?,?,?,?,?,?)'
            values = (self.user.username, item.title, dt, item.ISBN, item.quantity, max)    # All the values needed to insert into the Orders table
            cur.execute(sql, values)
            db.commit()

            sql = 'SELECT quantity FROM BOOKS WHERE ISBN=?'     # Get the old quantity in the Books table
            values = (item.ISBN,)
            cur.execute(sql, values)
            old_qty = cur.fetchone()[0]   # Old book quantity in inventory 
            new_qty = old_qty - item.quantity    # New qyantity to SET in the Books Table
            sql = 'UPDATE BOOKS SET quantity=? WHERE ISBN=?'   # Update the Books table quantity of each of the books in the cart.
            values = (new_qty, item.ISBN)
            cur.execute(sql, values)
            db.commit()
        self.empty(db) # Finally, empty the user's cart.




            
            
            
        

