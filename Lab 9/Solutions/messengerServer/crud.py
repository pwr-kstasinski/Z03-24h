import datetime

from sqlalchemy.orm import Session

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


def get_user(db: Session, user_id: int):
    return db.query(database_models.User).filter(database_models.User.id == user_id).first()


def get_user_by_nickname(db: Session, nick: str):
    return db.query(database_models.User).filter(database_models.User.nickname == nick).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database_models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password
    db_user = database_models.User(nickname=user.nickname, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database_models.Message).offset(skip).limit(limit).all()


def get_messages_by_users_id(db: Session, sender_id: int, recipient_id: int):
    messages = db.query(database_models.Message).filter_by(recipient_id=recipient_id, sender_id=sender_id).all()
    db.query(database_models.Message).filter_by(recipient_id=recipient_id, sender_id=sender_id). \
        delete(synchronize_session="fetch")
    db.commit()
    return messages


def create_message(db: Session, message: schemas.MessageCreate, recipient_id: int, sender_id: int):
    db_message = database_models.Message(**message.dict(), recipient_id=recipient_id, sender_id=sender_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
