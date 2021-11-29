from database_manager import create_connection, TABLES, init_database, DB_NAME, clear_all_db, remake_db
from classes.book import Book
from classes.user import User

def main():
    db = create_connection(DB_NAME)
    #clear_all_db(db)
    remake_db(db)
    #init_database(db, TABLES)


def menuing():
    db = create_connection(DB_NAME)
    run = True
    current_user = User(db)
    while run == True:
        # If the user is logged in: menu
        if current_user.logged_in:
            print("====================Main Menu====================\n")
            choice = '-1'
            while choice not in ['1', '2', '3', '4', '5', '6']:
                choice = input('1) View Cart\n2) Browse All Items in Inventory\n3) Browse Books by Genre\n4) Edit Account\n5) Delete Account\n6) Logout\nSelection: ')
                # View Cart
                if choice == '1':
                    print("====================Cart Options====================\n")
                    cart_choice = '-1'
                    current_user.view_cart()
                    while cart_choice not in ['1', '2', '3','4']:
                        cart_choice = input("1) Go back\n2) Remove Item\n3) Empty Cart\n4) Checkout\n Selection: ")
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
                            flag = current_user.cart.remove(index, qty)
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
                                        print("\nSuccess! You have checked out your cart.")
                            elif new_info_flag == '2':
                                cc = input("Enter your credit cart number: ")
                                cc_cvv = input("Enter your CVV: ")
                                confirm = input("\nFinal Confirmation: Do you wish to checkout?\n1) Yes\n2) No")
                                if confirm == '1':
                                    success = current_user.checkout()
                                    if success:
                                        print("\nSuccess! You have checked out your cart.")
                            choice = '-1'


                # Browse All
                elif choice == '2':
                    pass

                # Browse by genre
                elif choice == '3':
                    pass

                # Edit user account
                elif choice == '4':
                    print("\n====================Edit Account====================\n")
                    account_choice = '-1'
                    print(repr(current_user))
                    conf = '-1'
                    while account_choice not in ['1', '2', '3', '4', '5','6','7','8']:
                        account_choice = input("Select what you wish to alter:\n1) Name\n2) Username\n3) Password\n4) Address\n5) State\n6) City\n7) Zip\n8) Credit Card Information\nSelection: ")
                        # Edit Name info
                        if account_choice == '1':
                            new_first_name = input("\nEnter your first name: ")
                            new_last_name = input("Enter your last nbame ")
                            conf = input("\nApply changes?\n1) Yes\n2) No\nSelection: ")
                        # Edit Username info
                        elif account_choice == '2':
                            pass
                        # Edit Password info
                        if account_choice == '3':
                            pass
                        # Edit Address info
                        elif account_choice == '4':
                            pass
                        # Edit State info
                        if account_choice == '5':
                            pass
                        # Edit City info
                        elif account_choice == '6':
                            pass
                        # Edit Zip info
                        if account_choice == '7':
                            pass
                        # Edit Credit Card info
                        elif account_choice == '8':
                            pass



                # Delete user account
                elif choice == '5':
                    pass

                # Logout
                elif choice == '6':
                    pass



                
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
if __name__=="__main__":
    #main()
    #test()
    menuing()