import sqlite3 as db
from typing import Callable, List, Tuple 
from classes.book import Book
#===================================================================================================
# GLOBALS:
DB_NAME = "store.db"
USERS_TABLE = """CREATE TABLE IF NOT EXISTS Users (
                                        id TEXT PRIMARY KEY,
                                        username TEXT NOT NULL UNIQUE,
                                        first_name TEXT NOT NULL,
                                        last_name TEXT NOT NULL,
                                        password_salt TEXT NOT NULL,
                                        password_key TEXT NOT NULL,
                                        address TEXT NOT NULL,
                                        state TEXT NOT NULL,
                                        city TEXT NOT NULL,
                                        zip INTEGER NOT NULL,
                                        cc_number INTEGER NOT NULL,
                                        cc_cvv INTEGER NOT NULL
                                    );"""

ORDERS_TABLE = """CREATE TABLE IF NOT EXISTS Orders (
                                    id INTEGER PRIMARY KEY,
                                    username TEXT NOT NULL,
                                    title TEXT NOT NULL,
                                    date TEXT NOT NULL,
                                    ISBN TEXT NOT NULL,
                                    quantity INTEGER NOT NULL,
                                    order_number INTEGER NOT NULL,
                                    total_cost REAL NOT NULL,
                                    FOREIGN KEY (username) REFERENCES Users (username),
                                    FOREIGN KEY (ISBN) REFERENCES Books (ISBN)
                                );"""


CART_TABLE = """CREATE TABLE IF NOT EXISTS Cart (
                                    id INTEGER PRIMARY KEY,
                                    ISBN INTEGER NOT NULL,
                                    username TEXT NOT NULL,
                                    quantity INTEGER NOT NULL,
                                    FOREIGN KEY (username) REFERENCES Users (username),
                                    FOREIGN KEY (ISBN) REFERENCES Books (ISBN)
                                );"""

BOOKS_TABLE = """CREATE TABLE IF NOT EXISTS Books (
                                    ISBN INTEGER PRIMARY KEY,
                                    title TEXT NOT NULL,
                                    author TEXT NOT NULL,
                                    genre TEXT NOT NULL,
                                    format TEXT NOT NULL,
                                    price REAL NOT NULL,
                                    quantity INTEGER NOT NULL
                                );"""

TABLES = [USERS_TABLE, BOOKS_TABLE, ORDERS_TABLE, CART_TABLE]
DELETE_TABLES = ['DROP TABLE IF EXISTS Books', 'DROP TABLE IF EXISTS Users', 'DROP TABlE IF EXISTS Cart', 'DROP TABLE IF EXISTS Orders']



#===================================================================================================
# FUNCTIONS:
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = db.connect(db_file)
        return conn
    except db.Error as e:
        print(e)
    return conn




def delete_table(conn, sql):
    ''' Inverse of the create_table function
    Deletes the table based on the sql inputted.
    '''
    try:
        c = conn.cursor()
        c.execute(sql)
    except db.Error as e:
        print(e)



def drop_all(conn, tables):
    for table in tables:
        delete_table(conn, table)



def create_table(conn, table_command):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(table_command)
    except db.Error as e:
        print(e)


def init_database(conn, tables):
    for table in tables:
        create_table(conn, table)



# Function to clear every entry in every table of the database. 
# Really just so we can reset/repopulate db for testing/demonstrating app functionality.
def clear_all_db(conn):
    tables = ['Users', 'Orders', 'Books', 'Cart']
    for table_name in tables:
            sql = 'DELETE FROM ' + table_name
            conn.execute(sql)
            conn.commit()


# Function to populate the inventory full of pre-defined book items.
# Similar to above function, should be used to test/demonstrate app with ease.
def populate_inventory(books_to_add):
    for book in books_to_add:
        book.add_to_db()



# Function to completely reset the database to its default value. 
# Fills the database with 20 default books, all with 100 quantity to begin.
def reset_to_default(conn):
    clear_all_db(conn)
    init_database(conn, TABLES)
    # Books to initialize the database
    books = [Book(conn,100,2213,'The Hobbit',24.99,'J.R.R. Tolkien','Fantasy','Paperback'),\
        Book(conn,100,4590,'The Lion, The Which, And The Wardrobe', 14.99,'C.S. Lewis','Fiction','eBook'),\
        Book(conn,100,5113,'Nineteen Eighty-Four',19.99,'George Orwell','Dystopian','Hard Cover'),\
        Book(conn,100,7253,'Animal Farm', 9.99,'George Orwell','Allegorical Fiction','Paperback'),\
        Book(conn,100,1131,'To Kill a Mockingbird', 12.99,'Harper Lee', 'Historical Fiction','Hard Cover'),\
        Book(conn,100,1322,'Pride and Prejudice', 19.99,'Jane Austin','Historical Fiction','eBook'),\
        Book(conn,100,1733,'The Odyssey',17.99,'Homer','Philosophy','Paperback'),\
        Book(conn,100,3192,'Fahrenheit 451', 11.99, 'Ray Bradbury','Dystopian', 'eBook'),\
        Book(conn,100,7228,'Meditations',18.99,'Marcus Aurelius', 'Philosophy','Hard Cover'),\
        Book(conn,100,8090,'The Republic',13.99,'Plato','Philosophy','Paperback'),\
        Book(conn,100,1309,'The Great Gatsby',14.99,'F. Scott Fitzgerald','Historical Fiction','eBook'),\
        Book(conn,100,1792,'Lord of the Flies',19.99,'William Golding','Allegorical Fiction','eBook'),\
        Book(conn,100,4283,'The Scarlet Letter',8.99,'Nathaniel Hawthorne','Historical Fiction','eBook'),\
        Book(conn,100,6829,'The Secret Garden',12.99,'Frances Hodgson Burnett','Fiction','Hard Cover'),\
        Book(conn,100,7492,'War and Peace',18.99,'Leo Tolstoy','Historical Fiction','Hard Cover'),\
        Book(conn,100,1920,'The Prince',18.99,'Niccolò Machiavelli','Philosophy','Paperback'),\
        Book(conn,100,7812,'Frankenstein',22.99,'Mary Shelley','Fiction','Paperback'),\
        Book(conn,100,9972,'Brave New World',16.99,'Aldous Huxley','Dystopian','Hard Cover'),\
        Book(conn,100,6751,'Dracula',11.99,'Bram Stoker','Gothic Fiction', 'eBook'),\
        Book(conn,100,8847,'Adventures of Huckleberry Finn',10.99,'Mark Twain','Historical Fiction','Paperback')]
    populate_inventory(books)     # Populate db with books in the above list. 


def remake_db(conn):
    drop_all(conn, DELETE_TABLES)
    init_database(conn, TABLES)


