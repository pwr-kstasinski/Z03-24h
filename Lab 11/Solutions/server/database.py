from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_host = os.environ['DB_HOST']
db_port = os.environ['DB_PORT']

engine = create_engine(
    #"mariadb+mariadbconnector://root:1236@127.0.0.1:3306"
    #"mariadb+mariadbconnector://root:1236@db:3306"
    "mariadb+mariadbconnector://{}:{}@{}:{}".format(db_user, db_password, db_host, db_port)
)

create_str = "CREATE DATABASE IF NOT EXISTS %s ;" % ("messenger")
engine.execute(create_str)
engine.execute("USE messenger;")


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
