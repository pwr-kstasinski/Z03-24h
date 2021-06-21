from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import or_, and_

from datebase import Message, DB_Session


def add_message(msg: Message) -> bool:
    session = DB_Session()
    try:
        session.add(msg)
        session.commit()
    except:
        session.rollback()
        return False
    finally:
        session.close()
    return True


def get_messages(first_user_id: int, second_user_id: int) -> [Message]:
    session: Session = DB_Session()
    try:
        return session.query(Message).filter_by(group=False).filter(
            or_(
                and_(Message.receiver_id == first_user_id, Message.sender_id == second_user_id),
                and_(Message.receiver_id == second_user_id, Message.sender_id == first_user_id)
            )
        ).all()
    except:
        raise
        return []
    finally:
        session.close()


def get_group_messages(group_id: int) -> [Message]:
    session: Session = DB_Session()
    try:
        return session.query(Message).filter_by(receiver_id=group_id, group=True).all()
    except:
        return []
    finally:
        session.close()
