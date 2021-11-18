from database_manager import create_connection, TABLES, init_database, DB_NAME

def main():
    db = create_connection(DB_NAME)

if __name__=="__main__":
    main()