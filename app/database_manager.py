import sqlite3 as db
from typing import Callable, List, Tuple 

# GLOBALS:
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
                                        cc_cvv int NOT NULL
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
                                    ISBN INTEGER PRIMARY KEY,
                                    title TEXT NOT NULL,
                                    author TEXT NOT NULL,
                                    genre TEXT NOT NULL,
                                    format TEXT NOT NULL,
                                    price REAL NOT NULL,
                                    quantity INTEGER NOT NULL
                                );"""



TABLES = [USERS_TABLE, BOOKS_TABLE, ORDERS_TABLE, CART_TABLE]

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


def init_database(conn, *args):
    for arg in args:
        create_table(conn, arg)




# SQL simplification find for a generic table name and value:
# Returns a list of the rows held as tuples containing the individual elemnts of the rows.
def find_many(conn, table_name: str, value_name, value) -> List[Tuple]:
    find_str = 'SELECT * FROM ' + str(table_name) + ' WHERE ' + str(value_name) + '=' + str(value)
    try:
        cur = conn.cursor()
        cur.execute(find_str)
        rows = cur.fetchall()
        return rows
    except:
        print("Unkown error occured.")
        return False


# SQL simplification of insert into Books table.
def add_book(conn, values: Tuple[int, str, str, str, str, float, int]) -> int:

    sql = ''' INSERT INTO Books(ISBN,title,author,genre,format,price,quantity)
            VALUES(?,?,?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        return cur.lastrowid
    except:
        print('Unkown error occured.')
        return False


# SQL simplification of insert into Users.
def add_user(conn, values: Tuple[str, str, str, str, str, str, str, int, int, int]) -> int:
    
    sql = ''' INSERT INTO Users(username,first_name,last_name,password,address,state,city,zip,cc_number,cc_cvv)
            VALUES(?,?,?,?,?,?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        return cur.lastrowid
    except:
        print('Unkown error occured.')
        return False

# SQL simplification of insert into Orders table.
def add_order(conn, values: Tuple[str, str, str, str, str, int]) -> int:
    sql = ''' INSERT INTO Orders(username,title,date,ISBN,quantity,order_number)
            VALUES(?,?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        return cur.lastrowid
    except:
        print('Unkown error occured.')
        return False


#SQL simplification of insert into Cart table.
def add_to_cart(conn, values: Tuple[int, str, int]) -> int:
        sql = ''' INSERT INTO Cart(ISBN,username,quantity)
            VALUES(?,?,?) '''
        try:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()
            return cur.lastrowid
        except:
            print('Unkown error occured.')
            return False
