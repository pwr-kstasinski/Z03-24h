from typing import List

import datetime

from pydantic import BaseModel


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    recipient_id: int
    sender_id: int
    send_time: datetime.datetime
    viewed: bool

    class Config:
        orm_mode = True


class CommonMessage(MessageBase):
    id: int
    sender_id: int
    sender_nickname: int
    send_time: datetime.datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    nickname: str


class UserCreate(UserBase):
    password: str


class UserActive(UserBase):
    id: int
    lastActive: datetime.datetime
    active: bool

    class Config:
        orm_mode = True


class User(UserBase):
    messages: List[Message] = []
    active: bool

    class Config:
        orm_mode = True
