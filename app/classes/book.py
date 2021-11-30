# Lindsay


class Book():

    def __init__(self, db, quantity=0,ISBN=0,title='',price=0,author='',genre='',format='') -> None:
        self.quantity = quantity
        self.ISBN = ISBN
        self.title = title
        self.price = price
        self.author = author
        self.genre = genre
        self.format = format
        self.db = db

    def __repr__(self, index=''):
        if index != '':
            index = index+')'
        visual = '==============================================\n'
        visual += '| ' + index + ' ' + self.title + '\n----------------------------------------------\n| '
        visual += 'ISBN: ' + str(self.ISBN) + '\n| '
        visual += 'Author: ' + self.author + '\n| '
        visual += 'Genre: ' + self.genre + '\n| '
        visual += 'Format: ' + self.format +'\n| '
        visual += 'Price: $' + str(self.price) +'\n'
        visual += '----------------------------------------------\n| '
        visual += 'QUANTITY: ' + str(self.quantity) +'\n'
        visual += '=============================================='
        return visual


    # Function to update database to reflect change from this book object
    # Will remove the set quantity from this book, if quantity > database quantity, 
    # this function will set the database quantity to 0
    def remove_from_db(self):
        cur = self.db.cursor()
        sql = 'SELECT quantity FROM Books WHERE ISBN=?'
        value = (self.ISBN,)
        cur.execute(sql, value)
        db_book_qty = cur.fetchone()
        if db_book_qty is None:  # Book doesn't exist, return False
            return False
        new_qty = db_book_qty[0] - self.quantity
        if new_qty < 0:
            new_qty = 0
        sql = 'UPDATE Books SET quantity=? WHERE ISBN=?'
        values = (new_qty, self.ISBN)
        cur.execute(sql, values)
        self.db.commit()
        return True     # Successfully updated the database, return True



    # Function to add the current book to the database
    # First checks if book exists, if so updates qty, if not, makes a new book object
    def add_to_db(self):
        cur = self.db.cursor()
        sql = ''' SELECT quantity FROM Books WHERE ISBN=?'''
        value = (self.ISBN,)
        cur.execute(sql, value)
        db_book_qty = cur.fetchone()
        if db_book_qty is not None:     # This book already exists, just need to update the quantity
            new_quantity = self.quantity + db_book_qty[0]
            sql = ''' UPDATE Books SET quantity=? WHERE ISBN=?'''
            values = (new_quantity, self.ISBN)
            cur.execute(sql, values)
            self.db.commit()
            return True     # Successfully updated quantity, return true
        else:           # This book does not exist, insert it into the book table.
            sql = ''' INSERT INTO Books(ISBN, title, author, genre, format, price, quantity)
                VALUES(?,?,?,?,?,?,?) '''
            values = (self.ISBN, self.title, self.author, self.genre, self.format, self.price, self.quantity)
            cur.execute(sql, values)
            self.db.commit()
            return True     # Successfully added book, return True

