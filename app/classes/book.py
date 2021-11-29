# Lindsay


class Book():

    def __init__(self) -> None:
        self.quantity = 0
        self.ISBN = 0
        self.title = ''
        self.price = 0
        self.author = ''
        self.genre = ''
        self.format = ''

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


    def remove_from_db():
        pass


    def add_to_db(self, db):
        sql = 'INSERT INTO Books(quantity, ISBN, title, author, genre, bookFormat)'
        values = (self.quantity, self.ISBN, self.title, self.author, self.genre, self.format)
        sql = 'SET '

        # Add to db just adds the current book object to db

        # The other thing add book should do is check if the
        # book already exists in the database, and if so, 
        # just update the quantity