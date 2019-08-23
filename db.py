import os
import sqlite3

DB_PATH = 'immobiliare.sqlite'

def create_schema(conn):
    sql = '''CREATE TABLE IF NOT EXISTS 
             ADS(ID INTEGER PRIMARY KEY);
             CREATE TABLE IF NOT EXISTS
             ADS_FULL(ADID VARCHAR(16) PRIMARY KEY,TITLE TEXT, DESCRIPTION TEXT, PRICE INT, ROOMS VARCHAR(4), SIZE INT, BATHROOMS VARCHAR(4), LEVEL VARCHAR(4));
          '''
    conn.execute(sql)  # shortcut for conn.cursor().execute(sql)


def create_or_open_db(db_file=DB_PATH):
    db_is_new = not os.path.exists(db_file)
    conn = sqlite3.connect(db_file)
    if db_is_new:
        create_schema(conn)
    return conn


def get_data(conn):
    SQL = "SELECT ID FROM ADS2;"
    cur = conn.cursor()
    cur.execute(SQL)
    return cur;


def insert_data(conn, data):
    sql = "INSERT INTO ADS_FULL(ADID, TITLE, DESCRIPTION, PRICE, ROOMS, SIZE, BATHROOMS, LEVEL) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    #sql = "INSERT INTO ADS(ID) VALUES (?)"
    conn.executemany(sql, data)
    conn.commit()

