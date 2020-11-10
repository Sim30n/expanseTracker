import sqlite3
from sqlite3 import Error
import pandas as pd
from datetime import date
import sys

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query, values):
    cursor = connection.cursor()
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

connection = create_connection("transactions.sqlite")

create_transactions_table = """
CREATE TABLE IF NOT EXISTS transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT,
  description TEXT,
  amount FLOAT
);
"""
execute_query(connection, create_transactions_table, None)


def create_transaction(today, description, amount):
    if today == None:
        today = date.today()
    #s = "2020-11-11"
    sqlite_insert_with_param = """INSERT INTO transactions
                      (date, description, amount)
                      VALUES (?, ?, ?);"""
    data_tuple = (today, description, amount)
    execute_query(connection, sqlite_insert_with_param, data_tuple)

def update_transaction(id, description, amount):
    today = date.today()
    sqlite_insert_with_param = """UPDATE transactions
                      SET
                        date = ?,
                        description = ?,
                        amount = ?
                      WHERE
                        id = ?
                      """
    data_tuple = (today, description, amount, id)
    execute_query(connection, sqlite_insert_with_param, data_tuple)

def delete_transaction(id):
    del_transaction = """DELETE FROM transactions WHERE id = ?"""
    data_tuple = (id,)
    execute_query(connection, del_transaction, data_tuple)

def calculations():
    df = pd.read_sql_query("SELECT * FROM transactions", connection)
    total = df['amount'].sum()
    print("Total spent: {} €".format(total))
    df['date'] = pd.to_datetime(df['date'])
    daily = df.groupby(df['date'].dt.date).sum()
    daily_average = daily["amount"].mean(axis = 0)
    print("Daily average: {} €".format(daily_average))

def print_database():
    df = pd.read_sql_query("SELECT * FROM transactions", connection)
    print(df.to_string(index=False))

def read_me():
    try:
        f = open("README.md", "r")
        print(f.read())
        f.close()
    except FileNotFoundError:
        sys.exit(0)

def main():
    try:
        sys.argv[1]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <-a, -e, -d, -p, -c, -help>")
    argv_len = len(sys.argv)
    if sys.argv[1] == "-a" and argv_len == 4:
        create_transaction(None, sys.argv[2], float(sys.argv[3]))
    if sys.argv[1] == "-a" and argv_len == 5:
        create_transaction(sys.argv[2], sys.argv[3], float(sys.argv[4]))
    elif sys.argv[1] == "-p":
        print_database()
    elif sys.argv[1] == "-e":
        update_transaction(sys.argv[2], sys.argv[3], float(sys.argv[4]))
    elif sys.argv[1] == "-d":
        delete_transaction(sys.argv[2])
    elif sys.argv[1] == "-c":
        calculations()
    elif sys.argv[1] == "-help":
        read_me()

main()
connection.close()
