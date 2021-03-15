import mysql.connector


def db_conn():
    db = mysql.connector.Connect(host="localhost", user="root")
    cursor = db.cursor()
    return db, cursor


def db_conn2():
    db = mysql.connector.Connect(host="localhost", user="root", db="newsapidb")
    cursor = db.cursor()
    return db, cursor


def create_db():
    db, cursor = db_conn()
    try:
        cursor.execute("CREATE DATABASE newsapidb")
        print("Database newsapidb created.")
    except Exception as e:
        print(e)
    return


def create_table():
    db, cursor = db_conn2()
    try:
        cursor.execute("CREATE TABLE newsdata (title VARCHAR(255), description VARCHAR(355))")
        print("Table newsdata created.")
    except Exception as e:
        print(e)


create_db()
create_table()
