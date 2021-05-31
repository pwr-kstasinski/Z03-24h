import datetime
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_

import database_models
import schemas


def update_last_activity_of_user(db: Session, user_id: int):
    db.query(database_models.User).filter(database_models.User.id == user_id). \
        update({"lastActive": datetime.datetime.utcnow()}, synchronize_session='fetch')
    db.commit()


def get_active_users(db: Session):
    current_time = datetime.datetime.utcnow()
    active_period = current_time - datetime.timedelta(minutes=5, seconds=30)
    last_active_users = db.query(database_models.User).filter(
        database_models.User.lastActive > active_period).all()
    return last_active_users


def get_users_all(db: Session):
    return db.query(database_models.User).all()


def get_user(db: Session, user_id: int):
    return db.query(database_models.User).filter(database_models.User.id == user_id).first()


def get_user_by_nickname(db: Session, nick: str):
    return db.query(database_models.User).filter(database_models.User.nickname == nick).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database_models.User).offset(skip).limit(limit).all()


def mark_user_as_active(db: Session, user_id: int):
    db.query(database_models.User).filter(database_models.User.id == user_id). \
        update({"active": True}, synchronize_session='fetch')
    db.commit()


def unmark_user_as_active(db: Session, user_id: int):
    db.query(database_models.User).filter(database_models.User.id == user_id). \
        update({"active": False}, synchronize_session='fetch')
    db.commit()


"""
def get_ordered_users(db: Session, user_id: int):
    return db.query(database_models.User).order_by(database_models.User.messages)
    #database_models.User.messages)
"""  # .popularity.desc(),User.date_created.desc())


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password
    db_user = database_models.User(nickname=user.nickname, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database_models.Message).offset(skip).limit(limit).all()


def get_common_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database_models.CommonMessage).offset(skip).limit(limit).all()


def get_messages_by_users_id(db: Session, sender_id: int, recipient_id: int):
    messages = db.query(database_models.Message).filter_by(recipient_id=recipient_id, sender_id=sender_id).all()
    db.commit()
    return messages


def get_unread_messages_by_users_id(db: Session, sender_id: int, recipient_id: int):
    messages = db.query(database_models.Message).filter_by(
        recipient_id=recipient_id, sender_id=sender_id, viewed=False).order_by(database_models.Message.send_time).all()
    db.commit()
    return messages


# ordered by date
def get_conversation(db: Session, user_id: int, otherUser_id: int):
    messages = db.query(database_models.Message).filter(
        or_(
            and_(database_models.Message.recipient_id == user_id, database_models.Message.sender_id == otherUser_id),
            and_(database_models.Message.recipient_id == otherUser_id, database_models.Message.sender_id == user_id))). \
        order_by(database_models.Message.send_time).all()
    db.commit()
    return messages


def get_user_all_messages(db: Session, user_id: int):
    messages = db.query(database_models.Message).filter(
        or_(database_models.Message.recipient_id == user_id, database_models.Message.sender_id == user_id)).all()
    db.commit()
    return messages


def create_message(db: Session, message: schemas.MessageCreate, recipient_id: int, sender_id: int):
    db_message = database_models.Message(**message.dict(), recipient_id=recipient_id, sender_id=sender_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def create_common_message(db: Session, message: schemas.MessageCreate, sender_id: int, sender_nickname: str):
    db_message = database_models.CommonMessage(**message.dict(), sender_id=sender_id, sender_nickname=sender_nickname)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def mark_message_as_viewed(db: Session, message_id: int):
    message = db.query(database_models.Message).filter_by(id=message_id).update({"viewed": True}, synchronize_session='fetch')
    db.commit()
    return message

def mark_multiple_messages_as_viewed(db: Session, messages_ids: List[int]):
    messages = db.query(database_models.Message).filter(database_models.Message.id.in_(messages_ids)). \
        update({"viewed": True}, synchronize_session='fetch')
    db.commit()
    return messages
