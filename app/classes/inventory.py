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
        pass
    #called to display all entriesin BOOKS schema
    def display(self):
        #retrieves the title stock price format of every book in the BOOKS schema
        books = self.inv_cur().execute("SELECT title,stock,price,format FROM Book")
        #prints the table for the user to peruse the available inventory
        print(tabulate(books.fetchall(),headers=["TITLE",'STOCK','PRICE','FORMAT']))

    def displayBygenre(self,genre):
        query = "SELECT * FROM Books WHERE genre ='"+genre+"'"
        print(query)
        execution =self.inv_cur().execute(query)
        print(tabulate(execution.fetchall(),headers=["TITLE",'STOCK','PRICE','FORMAT']))

    def retrieveBook(self,ISBN):
        query = "SELECT title,price,author,genre,format,quantity FROM Books WHERE ISBN ="+str(ISBN)
        result = self.inv_cur().execute(query)
        if result == []:           
            return None
        else:
            resulttuple = result.fetchall()
            retrievedBook = Book()
            retrievedBook.ISBN = ISBN  
            retrievedBook.title = resulttuple[0][0]
            retrievedBook.price = resulttuple[0][1]
            retrievedBook.author  = resulttuple[0][2]
            retrievedBook.genre = resulttuple[0][3]
            retrievedBook.format = resulttuple[0][4] 
            return retrievedBook

    #called to update BOOKS schema when books are purhcased
    def update(self,isbn,quantity):
        query = "UPDATE BOOKS SET stock = stock +"+quantity +"WHERE isbn ="+isbn+""
        self.inv_cur().execute(query)
        self.connection.commit()