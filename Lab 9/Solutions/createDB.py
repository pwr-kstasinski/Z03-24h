import sqlite3
from sqlite3 import Error


def create_connection(database):
    connection = None
    try:
        connection = sqlite3.connect(database)
        return connection
    except Error as error:
        print(error)

    return connection


def create_table(connection, create_table_sql):
    try:
        c = connection.cursor()
        c.execute(create_table_sql)
    except Error as error:
        print(error)


def main():
    database = r"sqlite.db"
    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                        login text PRIMARY KEY,
                                        password text NOT NULL
                                ); """


    sql_create_messages_table = """CREATE TABLE IF NOT EXISTS messages (
                                    id integer PRIMARY KEY,
                                    fromUser text NOT NULL,
                                    toUser text NOT NULL,
                                    msg text NOT NULL
                                );"""
                                

    connection = create_connection(database)
    if not connection is None:
        create_table(connection, sql_create_users_table)
        create_table(connection, sql_create_messages_table)

if __name__ == '__main__':
    main()