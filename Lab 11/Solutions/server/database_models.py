from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME, Boolean
from sqlalchemy.orm import relationship

import datetime

from database import Base

user_nickname_length = 32
user_password_length = 32
message_length = 256

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(user_nickname_length), unique=True, index=True)
    hashed_password = Column(String(user_password_length))
    lastActive = Column(DATETIME, default=datetime.datetime.utcnow)
    active = Column(Boolean, default=False)

    messages = relationship("Message",
                            primaryjoin="or_(User.id==Message.recipient_id, User.id==Message.sender_id)",
                            cascade="all, delete")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(message_length))

    send_time = Column(DATETIME, default=datetime.datetime.utcnow)
    viewed = Column(Boolean, default=False)

    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    recipient = relationship("User", foreign_keys=recipient_id, back_populates="messages")
    sender = relationship("User", foreign_keys=sender_id, back_populates="messages")


class CommonMessage(Base):
    __tablename__ = "common_messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(message_length))

    send_time = Column(DATETIME, default=datetime.datetime.utcnow)

    sender_nickname = Column(String(user_nickname_length), ForeignKey("users.nickname"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
