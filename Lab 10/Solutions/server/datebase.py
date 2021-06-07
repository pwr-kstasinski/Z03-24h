import os
from datetime import datetime

from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship

engine = create_engine(f'sqlite:///{os.getcwd()}/messenger.db', connect_args={'check_same_thread': False})

# DB_Session: scoped_session = scoped_session(sessionmaker(autocommit=False,
#                                                          autoflush=False,
#                                                          bind=engine))
DB_Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
# Base.query = DB_Session.query_property()
Base.query = scoped_session(DB_Session).query_property()

group_members_table = Table('group_members', Base.metadata,
                            Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True),
                            Column('user_id', Integer, ForeignKey('users.id'), primary_key=True))

unread_message_table = Table('unread_message', Base.metadata,
                             Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
                             Column('message_id', Integer, ForeignKey('messages.id'), primary_key=True))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    groups = relationship("Group",
                          secondary=group_members_table,
                          back_populates="members",
                          lazy='subquery')

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __repr__(self):
        return f'<User: {self.id} {self.login}>'


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    owner_id = Column(Integer)
    members = relationship("User",
                           secondary=group_members_table,
                           back_populates="groups",
                           lazy='subquery')

    def __init__(self, name, owner_id):
        self.name = name
        self.owner_id = owner_id

    def __repr__(self):
        return f'<Group: {self.id} {self.name}>'


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receiver_id = Column(Integer, nullable=False)
    message = Column(String(255), nullable=False)
    group = Column(Boolean, default=False)
    date = Column(DateTime, default=datetime.now)
    # unread = relationship("User", secondary=unread_message_table, lazy="noload")

    def __init__(self, sender_id, receiver_id, message, group,):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message = message
        self.group = group

    def __repr__(self):
        return f'<Message: {self.id}>'


Base.metadata.create_all(bind=engine)
