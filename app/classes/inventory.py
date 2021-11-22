# Robbie
#python module to easily format database tables
from tabulate import tabulate

#inventory class to manage interactions with BOOKS schema in database
class inventory():
    #creates the object
    def __init__(self,cursor,conn):
        #create cursor from sqlite3 py module for executing queries
        self.inv_cur = cursor
        self.connection = conn
        pass
    #called to display all entriesin BOOKS schema
    def display(self):
        #retrieves the title stock price format of every book in the BOOKS schema
        books = self.inv_cur().execute("SELECT title,stock,price,format FROM BOOKS")
        #prints the table for the user to peruse the available inventory
        print(tabulate(books.fetchall(),headers=["TITLE",'STOCK','PRICE','FORMAT']))
    #called to update BOOKS schema when books are purhcased
    def update(self,isbn,quantity):
        query = "UPDATE BOOKS SET stock = stock +"+quantity +"WHERE isbn ="+isbn+""
        self.inv_cur().execute(query)
        self.connection.commit()

    
        
