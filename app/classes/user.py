# Connor
from classes.shopping_cart import ShoppingCart


class User():
    def __init__(self) -> None:
        self.first_name = ''
        self.last_name = ''
        self.username = ''
        self.address = ''
        self.city = ''
        self.state = ''
        self.zip = 0
        self.cart = ShoppingCart(self)
        self.logged_in = False
        self.payment_info = dict(cc=0, cc_cvv=0)

    
    def initialize_cart(self):
        pass

    def add_to_cart(self, index, qty):
        pass

    def empty_cart(self):
        pass

    def checkout(self):
        pass

    def view_cart(self):
        pass

    def create_account(self):
        pass

    def delete_account(self):
        pass



