from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME
from sqlalchemy.orm import relationship

import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    lastActive = Column(DATETIME, default=datetime.datetime.utcnow)

    messages = relationship("Message",
                            primaryjoin="or_(User.id==Message.recipient_id, User.id==Message.sender_id)",
                            cascade="all, delete")
    # messagesFrom = relationship("Message", primaryjoin="User.id==Message.sender_id")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)

    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    recipient = relationship("User", foreign_keys=recipient_id, back_populates="messages")
    sender = relationship("User", foreign_keys=sender_id, back_populates="messages")
