import sqlite3 as db

DB_NAME = "store.db"


USERS_TABLE = """CREATE TABLE IF NOT EXISTS Users (
                                    id TEXT PRIMARY KEY,
                                    username TEXT NOT NULL UNIQUE,
                                    first_name TEXT NOT NULL,
                                    last_name TEXT NOT NULL,
                                    password TEXT NOT NULL,
                                    address TEXT NOT NULL,
                                    state TEXT NOT NULL,
                                    city TEXT NOT NULL,
                                    zip int NOT NULL,
                                    cc_number int NOT NULL,
                                    cc_cvv int NOT NULL,
                                );"""

ORDERS_TABLE = """CREATE TABLE IF NOT EXISTS Orders (
                                    id INTEGER PRIMARY KEY,
                                    username TEXT NOT NULL,
                                    title TEXT NOT NULL,
                                    date TEXT NOT NULL,
                                    ISBN TEXT NOT NULL,
                                    quantity TEXT NOT NULL,
                                    order_number INTEGER NOT NULL,
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
                                    id INTEGER PRIMARY KEY,
                                    ISBN INTEGER NOT NULL,
                                    author TEXT NOT NULL,
                                    genre TEXT NOT NULL,
                                    format TEXT NOT NULL,
                                    price REAL NOT NULL,
                                    quantity INTEGER NOT NULL,
                                    FOREIGN KEY (username) REFERENCES Users (username),
                                    FOREIGN KEY (ISBN) REFERENCES Books (ISBN)
                                );"""






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


def init_database():
    pass
