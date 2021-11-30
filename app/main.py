from classes.inventory import Inventory
from database_manager import create_connection, TABLES, init_database, DB_NAME, clear_all_db, remake_db, reset_to_default
from classes.book import Book
from classes.user import User

def main():
    db = create_connection(DB_NAME)
    #clear_all_db(db)
    remake_db(db)
    #init_database(db, TABLES)


def menuing():
    db = create_connection(DB_NAME)
    inv = Inventory(db)
    run = True
    current_user = User(db)

    # Encapsulating this function for easier menuing overall (this will be used multiple times)
    def add_item_menu():
        print("\n================Add Item To Cart================\n")
        while True:
            isbn = input("Enter the ISBN: ")
            qty = input("Enter the quantity: ")
            try:
                isbn = int(isbn)
                qty = int(qty)
                book = inv.retrieveBook(isbn)
                return current_user.add_to_cart(book, qty)
            except:
                print("\nError, only valid choices please!")


    while run == True:
        # If the user is logged in: menu
        if current_user.logged_in:
            choice = '-1'
            while choice not in ['1', '2', '3', '4', '5', '6','7']:
                print("\n\n====================Main Menu====================\n")
                choice = input('1) View Cart\n2) Browse All Items in Inventory\n3) Browse Books by a Category\n4) Edit Account\n5) Delete Account\n6) View Past Orders\n7) Logout\nSelection: ')
                # View Cart
                if choice == '1':
                    print("====================Cart Options====================\n")
                    cart_choice = '-1'
                    current_user.view_cart()
                    while cart_choice not in ['1', '2', '3','4']:
                        cart_choice = input("\n1) Go back\n2) Remove Item\n3) Empty Cart\n4) Checkout\n Selection: ")
                        # Go back
                        if cart_choice == '1':
                            choice == '-1'
                        # Remove item
                        elif cart_choice == '2':
                            index = input("\nEnter the number of the cart item to remove: ")
                            qty = input("\nQuantity you wish to remove: ")
                            try:
                                index = int(index)
                                qty = int(qty)
                            except:
                                print("\nError, either index or quantity invalid.")
                                cart_choice = '-1'
                                continue
                            flag = current_user.cart.remove(index-1, qty)
                            if flag == True:
                                print('\nSuccess! Item removed from your cart.')
                            else:
                                print('\nAn unexpected error occured.')
                            cart_choice == '-1'
                        # Empty cart
                        elif cart_choice == '3':
                            current_user.empty_cart()
                            print('\nAll items removed from cart')
                            cart_choice = '-1'
                        # Checkout
                        elif cart_choice == '4':
                            confirm = '-1'
                            new_info_flag = input("\nWould you like to use your existing payment information?\n1) Yes\n2) No\nSelection: ")
                            if new_info_flag not in ['1','2']:
                                new_info_flag = input("Error, enter a valid selection: ")
                            if new_info_flag == '1':
                                confirm = input("\nFinal Confirmation: Do you wish to checkout?\n1) Yes\n2) No\nSelection: ")
                                if confirm == '1':
                                    success = current_user.checkout(verify=True)
                                    if success:
                                        print("\nSuccess! You have checked out your cart.\n")
                            elif new_info_flag == '2':
                                cc = input("Enter your credit cart number: ")
                                cc_cvv = input("Enter your CVV: ")
                                confirm = input("\nFinal Confirmation: Do you wish to checkout?\n1) Yes\n2) No")
                                if confirm == '1':
                                    success = current_user.checkout()
                                    if success:
                                        print("\nSuccess! You have checked out your cart.\n")
                            choice = '-1'


                # Browse All
                elif choice == '2':
                    print("\n====================Category Selection====================")
                    inv.displayAll()
                    browse_choice = '-1'
                    while browse_choice not in ['1','2']:
                        browse_choice = input("\n1) Go Back\n2) Add a Book\nSelection: ")
                        if browse_choice == '1':
                            choice = '-1'
                        elif browse_choice == '2':
                            worked = add_item_menu()
                            if worked == True:
                                print("\nSuccessfully added item(s) to your cart!\n")
                            browse_choice = '-1'

                # Browse by genre
                elif choice == '3':
                    print("\n====================Category Selection====================")
                    category_choice = '-1'
                    while category_choice not in ['1','2','3','4']:
                        category_choice = input("\n1) Go Back\n2) View By Genre\n3) View By Format\n4) View By Price\nSelection: ")

                        # Display by genre
                        if category_choice == '2':
                            genres = inv.displayGenres()
                            genre_choice = '-1'
                            genre_inds = []
                            for i in range(len(genres)):     # Arbitrarily long list of numbers for available choices.
                                genre_inds.append(str(i+1))
                            while genre_choice not in genre_inds:
                                genre_choice = input("Selection: ")
                            print()
                            inv.displayByGenre(genres[int(genre_choice)-1])   # Display by selected genre
                            add_choice = '-1'
                            while add_choice not in ['1','2']:
                                add_choice = input("\n1) Go Back\n2) Add Book\nSelection: ")
                                if add_choice == '1':
                                    category_choice = '-1'
                                elif add_choice == '2':
                                    worked = add_item_menu()
                                    if worked == True:
                                        print("\nSuccessfully added item(s) to your cart!\n")
                                    category_choice = '-1'

                        # Display by format
                        elif category_choice == '3':
                            formats = inv.displayFormats()
                            format_choice = '-1'
                            format_inds = []
                            for i in range(len(formats)):     # Arbitrarily long list of numbers for available choices.
                                format_inds.append(str(i+1))
                            while format_choice not in format_inds:
                                format_choice = input("Selection: ")
                            print()
                            inv.displayByFormat(formats[int(format_choice)-1])
                            add_choice = '-1'
                            while add_choice not in ['1','2']:
                                add_choice = input("\n1) Go Back\n2) Add Book\nSelection: ")
                                if add_choice == '1':
                                    category_choice = '-1'
                                elif add_choice == '2':
                                    worked = add_item_menu()
                                    if worked == True:
                                        print("\nSuccessfully added item(s) to your cart!\n")
                                    category_choice = '-1'

                        # Display by price
                        elif category_choice == '4':
                            prices = [(5, 9.99), (10, 14.99), (15,19.99), (20,25.99)]   # List of price ranges as tuples
                            print("\nPRICE RANGES:\n============================")
                            price_choice = '-1'
                            for count, price_range in enumerate(prices):
                                print("| "+str(count+1)+" $"+str(price_range[0])+'<-->'+str(price_range[1]))
                            while price_choice not in ['1','2','3','4']:
                                price_choice = input("Selection: ")
                            price_range = prices[int(price_choice)-1]
                            print()
                            inv.displayByPrice(price_range[0],price_range[1])
                            add_choice = '-1'
                            while add_choice not in ['1','2']:
                                add_choice = input("\n1) Go Back\n2) Add Book\nSelection: ")
                                if add_choice == '1':
                                    category_choice = '-1'
                                elif add_choice == '2':
                                    worked = add_item_menu()
                                    if worked == True:
                                        print("\nSuccessfully added item(s) to your cart!\n")
                                    category_choice = '-1'
                            


                # Edit user account
                elif choice == '4':
                    print("\n====================Edit Account====================\n")
                    account_choice = '-1'
                    print(repr(current_user))
                    while account_choice not in ['1', '2', '3', '4', '5','6','7','8', '9']:
                        conf = '-1'
                        account_choice = input("Select what you wish to alter:\n1) Go Back\n2) Name\n3) Username\n4) Password\n5) Address\n6) State\n7) City\n8) Zip\n9) Credit Card Information\nSelection: ")
                        # Edit Name info
                        if account_choice == '2':
                            new_first_name = input("\nEnter your first name: ")
                            new_last_name = input("Enter your last name ")
                            conf = input("\nApply changes?\n1) Yes\n2) No\nSelection: ")
                            if conf == '1':
                                current_user.first_name = new_first_name
                                current_user.last_name = new_last_name
                                current_user.update_account()
                                print("\nSuccessfully changed your name information!\n")
                            else:
                                print("\nChanges reverted.\n")
                            account_choice = '-1'
                        # Edit Username info
                        elif account_choice == '3':
                            new_username = input('\nEnter your new username: ')
                            conf = input("\nApply changes?\n1) Yes\n2) No\nSelection: ")
                            if conf == '1':
                                current_user.username = new_username
                                current_user.update_account()
                                print("\nSuccessfully changed your username.\n")
                            else:
                                print("\nChanges reverted.\n")
                            account_choice = '-1'
                        # Edit Password info
                        if account_choice == '4':
                            new_password1 = input('\nEnter your new password: ')
                            new_password2 = input('Confirm your new password: ')
                            while new_password1 != new_password2:
                                print("\nError, passwords do not match")
                                new_password1 = input('\nEnter your new password: ')
                                new_password2 = input('\nConfirm your new password: ')
                            conf = input("\nApply changes?\n1) Yes\n2) No\nSelection: ")
                            if conf == '1':
                                current_user.update_password(new_password1)
                                print("\nSuccessfully changed your password.\n")
                            else:
                                print("\nChanges reverted.\n")
                            account_choice = '-1'
                        # Edit Address info
                        elif account_choice == '5':
                            new_address= input("\nEnter your address: ")
                            conf = input("\nApply changes?\n1) Yes\n2) No\nSelection: ")
                            if conf == '1':
                                current_user.address = new_address
                                current_user.update_account()
                                print("\nSuccessfully changed your address!\n")
                            else:
                                print("\nChanges reverted.\n")
                            account_choice = '-1'
                        # Edit State info
                        if account_choice == '6':
                            new_state = input("\nEnter your state: ")
                            conf = input("\nApply changes?\n1) Yes\n2) No\nSelection: ")
                            if conf == '1':
                                current_user.state = new_state
                                current_user.update_account()
                                print("\nSuccessfully changed your state information!\n")
                            else:
                                print("\nChanges reverted.\n")
                            account_choice = '-1'
                        # Edit City info
                        elif account_choice == '7':
                            new_city = input("\nEnter your city: ")
                            conf = input("\nApply changes?\n1) Yes\n2) No\nSelection: ")
                            if conf == '1':
                                current_user.city = new_city
                                current_user.update_account()
                                print("\nSuccessfully changed your city!\n")
                            else:
                                print("\nChanges reverted.\n")
                            account_choice = '-1'
                        # Edit Zip info
                        if account_choice == '8':
                            new_zip = input("\nEnter your zip: ")
                            try: 
                                new_zip = int(new_zip)
                                conf = input("\nApply changes?\n1) Yes\n2) No\nSelection: ")
                                if conf == '1':
                                    current_user.zip = new_zip
                                    current_user.update_account()
                                    print("\nSuccessfully changed your name information!\n")
                                else:
                                    print("\nChanges reverted.\n")
                                account_choice = '-1'
                            except:
                                print("\nError, invalid choice, please only integers.\n")
                            account_choice = '-1'
                        # Edit Credit Card info
                        elif account_choice == '9':
                            new_cc_number = input("\nEnter your credit card number: ")
                            new_cc_cvv = input("Enter your credit card CVV: ")
                            try: 
                                new_cc_number = int(new_cc_number)
                                new_cc_cvv = int(new_cc_cvv)
                                conf = input("\nApply changes?\n1) Yes\n2) No\nSelection: ")
                                if conf == '1':
                                    current_user.payment_info["cc"] = new_cc_number
                                    current_user.payment_info["cc_cvv"] = new_cc_cvv
                                    current_user.update_account()
                                    print("\nSuccessfully changed your name information!\n")
                                else:
                                    print("\nChanges reverted.\n")
                                print("\nError, invalid choice, please only integers.\n")
                                account_choice = '-1'
                            except:
                                print("\nError, invalid choice, please only integers.\n")
                                account_choice = '-1'



                # Delete user account
                elif choice == '5':
                    print('\n====================Delete Account====================')
                    delete_choice = '-1'
                    while delete_choice not in ['1','2']:
                        delete_choice = input("\nAre you sure you want to delete your account?\nThis means all order data and cart data associated with this account.\n1) Yes, I'm Sure\n2) No, Take me back\nSelection: ")
                        if delete_choice == '1':
                            print("\nI thought I made it clear that this was clearly the WRONG answer, let me try one more time.")
                            print("Are you SURE you want to delete your account???")
                            delete_choice2 = input("1) Yes, Forget Reason\n2) No, I Have a Brain\nSelection: ")
                            while delete_choice2 not in ['1','2']:
                                delete_choice2 = input("Enter a valid selection please: ")
                            if delete_choice2 == '1':
                                pw = input("Fine you crazy person, enter your password to delete your account: ")
                                if current_user.check_password(pw) == True:
                                    current_user.delete_account()
                                else:
                                    print("Wow, lucked out there, you input the wrong password. If you want to try again though I can't stop you")
                                    delete_choice2 = '-1'
                            elif delete_choice2 == '2':
                                print("\nGood move\n")
                                choice = '-1'
                        elif delete_choice == '2':
                            choice = '-1'
                

                # Show Past Orders
                elif choice == '6':
                    orders_choice = '-1'
                    print("\n====================Order History====================")
                    valid_orders = current_user.display_order_history()
                    while orders_choice not in ['1','2']:
                        if bool(valid_orders) == False:     # If user has no order history yet
                            print("\nYou have no orders yet!\n")     
                            choice = '-1'
                            break
                        orders_choice = input("\n1) Go Back\n2) View Specific Order\nSelection: ")
                        if orders_choice == '1':
                            choice = '-1'
                        elif orders_choice == '2':
                            specified_order = '-1'
                            while specified_order not in valid_orders:
                                specified_order = input("Please enter an order number to view that order: ")
                            current_user.display_specific_order(specified_order)
                            orders_choice = '-1'

                    

                # Logout
                elif choice == '7':
                    current_user.logout()



                
        # If the user is not logged in: menu
        else:
            print("====================Main Menu====================\n")
            choice = '-1'
            while choice not in ['1', '2', '3']:
                choice = input("1) Login\n2) Create Account\n3) Exit Program \nEnter your choice: ")
            if choice == '1':
                print("\n====================Login====================\n")
                current_user.username = input("Enter your username: ")
                pw = input("Enter your password: ")
                if current_user.login(pw):
                    pw = ''
                    continue
                else: 
                    pw = ''
                    choice = '-1'
            elif choice == '2':
                print("====================Register====================\n")
                current_user.create_account()
                continue
            elif choice == '3':
                run = False



# Tests for the shopping cart class (to be deleted)
def test():
    db = create_connection(DB_NAME)
    user1 = User(db)
    user1.create_account()
    user1.logout
    user1.username = 'tmh'
    user1.login('12')
    remake_db(db)



    print('\n\n')
    book = Book()
    book.ISBN = 12345
    book.title = 'The Lion, The Which, And The Wardrobe'
    book.author = 'C.S. Lewis'
    book.genre =  'fiction'
    book.quantity = 14
    book.price = 14.23
    book.format = 'e-Book'
    #print(book.__repr__())
    cur = db.cursor()
    sql = 'INSERT INTO Books(ISBN, title, author, genre, format, price, quantity) VALUES(?,?,?,?,?,?,?)'
    vals = (book.ISBN, book.title, book.author, book.genre, book.format, book.price, book.quantity)
    cur.execute(sql, vals)
    db.commit()


    user = User(db)
    user.username = 'tannermhess'
    user.payment_info['cc'] = 1234123412341234
    user.payment_info['cc_cvv'] = 111
    work = user.cart.add(book, 10)
    print(str(work))
    sql = 'SELECT * FROM Cart WHERE username=?'
    values = (user.username,)
    cur.execute(sql, values)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    user.view_cart()

    worked = user.cart.add(book, 4)
    sql = 'SELECT * FROM Cart WHERE username=?'
    print(str(worked))
    values = (user.username,)
    cur.execute(sql, values)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    user.view_cart()

    worked = user.cart.remove(0, 2)
    sql = 'SELECT * FROM Cart WHERE username=?'
    print(str(worked))
    values = (user.username,)
    cur.execute(sql, values)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    user.view_cart()

    worked = user.cart.remove(0, 15)
    sql = 'SELECT * FROM Cart WHERE username=?'
    print(str(worked))
    values = (user.username,)
    cur.execute(sql, values)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    user.view_cart()


    worked = user.cart.add(book, 4)
    print(str(worked))
    worked = user.cart.empty()
    sql = 'SELECT * FROM Cart WHERE username=?'
    print(str(worked))
    values = (user.username,)
    cur.execute(sql, values)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    user.cart.display_cart()

    user.cart.add(book, 8)
    user.cart.remove(0,5)
    user.cart.display_cart()
    user.cart.checkout()
    user.cart.display_cart()
    sql = 'SELECT * FROM Orders WHERE username=?'
    values = (user.username,)
    cur.execute(sql, values)
    rows = cur.fetchall()
    for row in rows:
        print(row)




def book_test():
    db = create_connection(DB_NAME)
    reset_to_default(db)
    cur = db.cursor()
    inv = Inventory(db)
    print('\n')
    inv.displayAll()
    inv.displayByAuthor('George Orwell')
    inv.displayFormats()
    inv.displayGenres()
    #print(cur.fetchall())


if __name__=="__main__":
    #main()
    #test()
    menuing()
    #book_test()