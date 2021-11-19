from database_manager import create_connection, TABLES, init_database, DB_NAME, add_to_cart

def main():
    db = create_connection(DB_NAME)
    add_to_cart(db, (1234, 'tannermhess', 1))
    cur = db.cursor()
    values = (1234,)
    sql = 'SELECT quantity FROM Cart WHERE ISBN=?'
    cur.execute(sql,values)
    value=cur.fetchone()[0]
    print(value)
    cur.execute("SELECT * FROM Cart")
    values = cur.fetchall()
    for val in values:
        print(val)
    cur.execute("DELETE FROM Cart")
    db.commit()
if __name__=="__main__":
    main()