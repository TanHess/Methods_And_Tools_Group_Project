# Robbie
#python module to easily format database tables
from tabulate import tabulate
from classes.book import Book 
#inventory class to manage interactions with BOOKS schema in database
class Inventory():
    #creates the object
    def __init__(self,conn):
        #create cursor from sqlite3 py module for executing queries
        self.inv_cur = conn.cursor
        self.connection = conn

    #called to display all entriesin BOOKS schema
    def displayAll(self):
        #retrieves the title stock price format of every book in the BOOKS schema
        books = self.inv_cur().execute("SELECT title,ISBN,quantity,price,format FROM Books")
        #prints the table for the user to peruse the available inventory
        print(tabulate(books.fetchall(),headers=["TITLE",'ISBN','STOCK','PRICE','FORMAT']))

    def displayByGenre(self,genre):
        query = "SELECT ISBN FROM Books WHERE genre ='"+genre+"'"
        cur = self.connection.cursor()
        cur.execute(query)
        index = 1
        results = cur.fetchall()
        for isbn in results:
            book = self.retrieveBook(isbn[0])
            print(book.__repr__(str(index)))
            index += 1

    def displayByFormat(self, format):
        query = "SELECT ISBN FROM Books WHERE format ='"+format+"'"
        cur = self.connection.cursor()
        cur.execute(query)
        index = 1
        results = cur.fetchall()
        for isbn in results:
            book = self.retrieveBook(isbn[0])
            print(book.__repr__(str(index)))
            index += 1
    
    def displayByPrice(self, min, max):
        query = "SELECT ISBN FROM Books WHERE price BETWEEN "+str(min)+" AND "+str(max)+" ORDER BY price"
        cur = self.connection.cursor()
        cur.execute(query)
        index = 1
        results = cur.fetchall()
        for isbn in results:
            book = self.retrieveBook(isbn[0])
            print(book.__repr__(str(index)))
            index += 1
    

    # Display all available genres in the database
    def displayGenres(self):
        print("\nGENRES:")
        query = "SELECT DISTINCT genre FROM Books"
        cur = self.connection.cursor()
        cur.execute(query)
        index = 1
        results = cur.fetchall()
        genres = []
        print("============================")
        for genre in results:
            print('| '+str(index)+ ') ' +genre[0])
            index += 1
            genres.append(genre[0])
        print("============================")
        return genres

    # Display all available formats in the database.
    def displayFormats(self):
        print("\nFORMATS:")
        query = "SELECT DISTINCT format FROM Books"
        cur = self.connection.cursor()
        cur.execute(query)
        index = 1
        results = cur.fetchall()
        formats = []
        print("============================")
        for format in results:
            print('| '+str(index)+ ') ' +format[0])
            index += 1
            formats.append(format[0])
        print("============================")
        return formats


    def retrieveBook(self,ISBN):
        query = "SELECT title,price,author,genre,format,quantity FROM Books WHERE ISBN ="+str(ISBN)
        result = self.inv_cur().execute(query)
        results=result.fetchone()
        if results == None:           
            return None
        else:
            resulttuple = results
            retrievedBook = Book(self.connection)
            retrievedBook.ISBN = ISBN  
            retrievedBook.title = resulttuple[0]
            retrievedBook.price = resulttuple[1]
            retrievedBook.author  = resulttuple[2]
            retrievedBook.genre = resulttuple[3]
            retrievedBook.format = resulttuple[4]
            retrievedBook.quantity = resulttuple[5] 
            return retrievedBook

    #called to update BOOKS schema when books are purchased
    def update(self,isbn,quantity):
        query = "UPDATE Books SET quantity = stock +"+quantity +"WHERE isbn ="+isbn+""
        self.inv_cur().execute(query)
        self.connection.commit()