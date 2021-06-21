from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pprint import pprint

import os
import mariadb
import sys
import time


db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_host = os.environ['DB_HOST']
db_port = os.environ['DB_PORT']
db_name = os.environ['DB_NAME']

# Connect to MariaDB Platform
connection_number = 0
__max_connection_number__ = 5
__time_delay_for_retry__ = 5

conn = None
while True:
    try:
        conn = mariadb.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=int(db_port)
        )
        break
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        if connection_number < __max_connection_number__:
            time.sleep(__time_delay_for_retry__)
        else:
            sys.exit(1)
        connection_number = connection_number + 1

# Get Cursor
cur = conn.cursor()

create_str = "CREATE DATABASE IF NOT EXISTS {} ;".format(db_name)
cur.execute(create_str)
conn.commit()
conn.close()

engine = create_engine(
    #"mariadb+mariadbconnector://root:1236@127.0.0.1:3306"
    "mariadb+mariadbconnector://{}:{}@{}:{}/{}".format(db_user, db_password, db_host, db_port, db_name)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
