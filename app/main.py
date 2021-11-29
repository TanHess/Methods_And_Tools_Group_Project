from database_manager import create_connection, TABLES, init_database, DB_NAME, clear_all_db, remake_db
from classes.book import Book
from classes.user import User

def main():
    db = create_connection(DB_NAME)
    #clear_all_db(db)
    remake_db(db)
    #init_database(db, TABLES)


def menuing():
    run = True
    current_user = User()
    while run == True:
        print("====================Main Menu====================")
        # If the user is logged in: menu
        if current_user.logged_in:
            pass
        # If the user is not logged in: menu
        else:
            choice = -1
            while choice not in [1, 2, 3]:
                choice = input("1) Login\n2) Logout\n3) Exit Program \nEnter your choice: ")
            if choice == 1:
                pass
            elif choice == 2:
                pass
            elif choice == 3:
                run = False



# Tests for the shopping cart class (to be deleted)
def test():
    db = create_connection(DB_NAME)
    user1 = User(db)
    user1.create_account()
    user1.logout
    user1.username = 'tmh'
    user1.password = '1'
    user1.login()



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
    main()
    test()