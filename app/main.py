from database_manager import create_connection, TABLES, init_database, DB_NAME, add_to_cart
from classes.book import Book
from classes.user import User

def main():
    db = create_connection(DB_NAME)
    add_to_cart(db, (1234, 'tannermhess', 1))
    cur = db.cursor()
    values = (1234,)
    sql = 'SELECT quantity FROM Cart WHERE ISBN=?'
    cur.execute(sql,values)
    value=cur.fetchone()[0]
    print(value)
    cur.execute("SELECT * FROM Cart")
    values = cur.fetchall()
    for val in values:
        print(val)
        
    cur.execute("DELETE FROM Cart")
    cur.execute("DELETE FROM Books")
    db.commit()




# Tests for the shopping cart class (to be deleted)
def test():
    print('\n\n')
    db = create_connection(DB_NAME)
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


    user = User()
    user.username = 'tannermhess'
    user.payment_info['cc'] = 1234123412341234
    user.payment_info['cc_cvv'] = 111
    work = user.cart.add(book, 10, db)
    print(str(work))
    sql = 'SELECT * FROM Cart WHERE username=?'
    values = (user.username,)
    cur.execute(sql, values)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    user.cart.display_cart()

    worked = user.cart.add(book, 4, db)
    sql = 'SELECT * FROM Cart WHERE username=?'
    print(str(worked))
    values = (user.username,)
    cur.execute(sql, values)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    user.cart.display_cart()

    worked = user.cart.remove(0, 2, db)
    sql = 'SELECT * FROM Cart WHERE username=?'
    print(str(worked))
    values = (user.username,)
    cur.execute(sql, values)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    user.cart.display_cart()

    worked = user.cart.remove(0, 15, db)
    sql = 'SELECT * FROM Cart WHERE username=?'
    print(str(worked))
    values = (user.username,)
    cur.execute(sql, values)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    user.cart.display_cart()


    worked = user.cart.add(book, 4, db)
    print(str(worked))
    worked = user.cart.empty(db)
    sql = 'SELECT * FROM Cart WHERE username=?'
    print(str(worked))
    values = (user.username,)
    cur.execute(sql, values)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    user.cart.display_cart()


    user.cart.checkout(db)
    user.cart.display_cart()

if __name__=="__main__":
    main()
    test()