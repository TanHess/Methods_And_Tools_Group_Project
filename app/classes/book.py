# Lindsay


class Book():

    def __init__(self, db) -> None:
        self.quantity = 0
        self.ISBN = 0
        self.title = ''
        self.price = 0
        self.author = ''
        self.genre = ''
        self.format = ''
        self.db = db

    def __repr__(self):
        visual = '==============================================\n'
        visual += '| ' + self.title + '\n----------------------------------------------\n| '
        visual += 'ISBN: ' + str(self.ISBN) + '\n| '
        visual += 'Author: ' + self.author + '\n| '
        visual += 'Genre: ' + self.genre + '\n| '
        visual += 'Format: ' + self.format +'\n| '
        visual += 'Price: $' + str(self.price) +'\n'
        visual += '----------------------------------------------\n| '
        visual += 'QUANTITY: ' + str(self.quantity) +'\n'
        visual += '=============================================='
        return visual


    def remove_from_db(self, db, ISBN):
        cur = db.cursor()
        sql = 'DELETE FROM Books WHERE ISBN=?'
        cur.execute(sql, (self.ISBN,))
        db.commit()


    def add_to_db(self, quantity, ISBN, title, author, genre, bookFormat, db):
        self.quantity = quantity
        self.ISBN = ISBN
        self.title = title
        self.price = price
        self.author = author
        self.genre = genre
        self.format = bookFormat
        
        cur = db.cursor()
        sql = ''' INSERT INTO Books(quantity, ISBN, title, author, genre, bookFormat)
            VALUES(?,?,?,?,?,?) '''
        values = (self.quantity, self.ISBN, self.title, self.price, self.author, self.genre, self.format)
        cur.execute(sql, values)
        db.commit()

