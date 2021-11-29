# Connor
from .shopping_cart import ShoppingCart
import hashlib
import os


class User():
    def __init__(self, db) -> None:
        self.first_name = ''
        self.last_name = ''
        self.username = ''
        self.address = ''
        self.city = ''
        self.state = ''
        self.zip = 0
        self.logged_in = False
        self.payment_info = {"cc": 0, "cc_cvv": 0}
        self.pwd_info = {"salt": 0, "key": 0}
        self.db = db
        self.cart = ShoppingCart(self, db=self.db)

    def __repr__(self):
        visual = '==============================================\n'
        visual += 'First Name: ' + self.first_name + '\n| '
        visual += 'Last Name: ' + self.last_name+ '\n| '
        visual += 'Username: ' + self.username + '\n| '
        visual += 'Address: ' + self.address +'\n| '
        visual += 'State: ' + self.state +'\n'
        visual += 'Zip: ' + self.zip + '\n| '
        visual += 'Credit Card Number: ' + str(self.payment_info.get('cc')) + 'CVV: ' + str(self.payment_info.get('cc_cvv')) + '\n| '
        visual += '=============================================='
        return visual
    
    def initialize_cart(self):
        self.cart.get_cart()

    def add_to_cart(self, book, qty):
        self.cart.add(self, book, qty)

    def empty_cart(self):
        self.cart.empty()

    def checkout(self, verify=False):
        self.cart.checkout(verify)

    def view_cart(self):
        self.cart.display_cart()

    def check_username(self, username):
        cur = self.db.cursor()
        sql = 'SELECT username FROM Users WHERE username=?'
        cur.execute(sql, (username,))
        account = cur.fetchone()
        if account == None:
            return True
        else: 
            return False

    def hash_password(self, password):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        self.pwd_info["salt"] = salt
        self.pwd_info["key"] = key

    def create_account(self):
        print("Please fill out the info to create your account")
        confirm = '-1'
        while confirm != '1':
            self.first_name = input("First Name: ")
            self.last_name = input("Last Name: ")
            username = input("Username: ")
            if self.check_username(username):
                self.username = username
            else:
                while not self.check_username(username):
                    print("Username taken!")
                    username = input("Username: ")
                self.username = username
            password1 = input("Password: ")
            password2 = input("Confirm Password: ")     
            while password1 != password2:           # Confirm the passwords match. 
                print("Error, passwords do not match!")
                password1 = input("Password: ")
                password2 = input("Confirm Password: ")
            self.hash_password(password1)
            self.address = input("Street: ")
            self.city = input("City: ")
            self.state = input("State: ")
            self.zip = input("Zip: ")
            self.payment_info["cc"] = input("Credit Card Number: ")
            self.payment_info["cc_cvv"] = input("CVV: ")
            print("Ensure that all of your info is correct:")
            print(repr(self))   # Print the user data in a readable way
            confirm = input('\n1) Yes, this is correct\n2) No, go back\n Selection: ') # Give user option to go back and change info.
            while confirm not in ['1', '2']:
                confirm = input('Error! Please enter a valid selection!\n Selection: ')

        cur = self.db.cursor()
        sql = ''' INSERT INTO Users(first_name, last_name, username, password_salt, password_key, address, city, state, zip, cc_number, cc_cvv)
            VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
        values = (self.first_name, self.last_name, self.username, self.pwd_info.get("salt"), self.pwd_info.get("key"), self.address, self.city, self.state, self.zip, self.payment_info.get("cc"), self.payment_info.get("cc_cvv"))
        cur.execute(sql, values)
        self.db.commit()

    def delete_account(self):
        cur = self.db.cursor()
        sql = 'DELETE FROM Users WHERE username=?'
        cur.execute(sql, (self.username,))
        self.db.commit()

    def login(self, password):
        cur = self.db.cursor()
        sql = 'SELECT username, password_salt, password_key FROM Users WHERE username=?'
        cur.execute(sql, (self.username,))
        account = cur.fetchone()
        if account == None:
            print("Either the username or password is incorrect!")
            return

        username = account[0]
        salt = account[1]
        key = account[2]
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

        if key == new_key:
            sql = 'SELECT first_name, last_name, address, city, state, zip, cc_number, cc_cvv FROM Users WHERE username=?'
            cur.execute(sql, (username,))
            account = cur.fetchone()
            self.first_name = account[0]
            self.last_name = account[1]
            self.username = username
            self.address = account[2]
            self.city = account[3]
            self.state = account[4]
            self.zip = account[5]
            self.cart = ShoppingCart(self, db=self.db)
            self.logged_in = True
            self.payment_info = {"cc": account[6], "cc_cvv": account[7]}
            self.pwd_info = {"salt": salt, "key": key}
            self.initialize_cart()
            print("Successfully logged in!")
            return True
        else:
            print("Either the username or password is incorrect!")
            return False

    def logout(self):
        self.first_name = ''
        self.last_name = ''
        self.username = ''
        self.address = ''
        self.city = ''
        self.state = ''
        self.zip = 0
        self.cart = ShoppingCart(self)
        self.logged_in = False
        self.payment_info = {"cc": 0, "cc_cvv": 0}
        self.pwd_info = {"salt": 0, "key": 0}



