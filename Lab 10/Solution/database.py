import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(f'sqlite:///{os.getcwd()}\\database.db',
                       convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(255), unique=True)
    password = Column(String(255))
    active = Column(Integer)

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __repr__(self):
        return f'<User:{self.id} {self.login}>'


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer)
    recipient_id = Column(Integer)
    content = Column(String(255))
    sent = Column(DateTime)
    read = Column(Integer)

    def __init__(self, sender_id, recipient_id, content):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.content = content
        self.sent = datetime.now()
        self.read = 0

    def __repr__(self):
        return f'<Message:{self.id}>'
