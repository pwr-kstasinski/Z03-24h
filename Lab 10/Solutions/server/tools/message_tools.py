from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import or_, and_, insert, delete, text

from datebase import Message, DB_Session, unread_message_table
from tools import group_tools, user_tools


def add_message(msg: Message) -> bool:
    session: Session = DB_Session()

    try:
        session.add(msg)
        session.flush()
        session.refresh(msg)
    except Exception as e:
        session.rollback()
        session.close()
        return False
    list = []
    if msg.group:
        users_list = None
        if msg.receiver_id == 0:
            users_list = user_tools.get_users()
        else:
            users_list = group_tools.get_group(msg.receiver_id).members
        if users_list:
            for u in users_list:
                if u.id != msg.sender_id:
                    list.append({'user_id': u.id, 'message_id': msg.id})
    else:
        list.append({'user_id': msg.receiver_id, 'message_id': msg.id})

    try:
        if len(list) > 0:
            stat = insert(unread_message_table).values(list)
            session.execute(stat)
        session.commit()
    except Exception as e:
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


def update_messages_status(messages_id: [int], user_id: int):
    session: Session = DB_Session()
    try:
        stmt = delete(unread_message_table).where(and_(unread_message_table.c.user_id == user_id,
                                                       unread_message_table.c.message_id.in_(
                                                           messages_id)))
        # session.delete(mess)
        session.execute(stmt)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
    finally:
        session.close()
    return False


def get_unread_messages(user_id: int):
    session: Session = DB_Session()
    print(user_id)
    try:
        return session.query(unread_message_table).filter_by(user_id=user_id).all()
    except:
        return []
    finally:
        session.close()


def get_all_unread_messages():
    session: Session = DB_Session()
    try:
        return session.query(unread_message_table).all()
    except:
        return []
    finally:
        session.close()

def get_message_by_id(message_id: int) -> Message:
    session: Session = DB_Session()

    try:
        return session.query(Message).filter_by(id=message_id).one()
    except:
        return None
    finally:
        session.close()


def get_last_message_user(first_user_id: int, second_user_id: int):
    session: Session = DB_Session()
    try:
        return session.query(Message).filter(
            and_(
                or_(
                    and_(Message.receiver_id == first_user_id, Message.sender_id == second_user_id),
                    and_(Message.receiver_id == second_user_id, Message.sender_id == first_user_id)
                ),
                Message.group == False
            )).order_by(Message.id.desc()).first()
    except Exception as e:
        return None
    finally:
        session.close()


def get_last_message_group(group_id: int):
    session: Session = DB_Session()
    try:
        return session.query(Message).filter_by(receiver_id=group_id, group=True).order_by(Message.date.desc()).first()
    except Exception as e:
        return None
    finally:
        session.close()


def get_number_of_unread_message_user(user_id: int, sender_id: int) -> int:
    session: Session = DB_Session()

    try:
        return session.query(func.count(unread_message_table.c.message_id)) \
            .join(Message, Message.id == unread_message_table.c.message_id, isouter=True) \
            .filter(unread_message_table.c.user_id == user_id, Message.receiver_id == user_id,
                    Message.sender_id == sender_id, Message.group == False).first()[0]

        # stmt = text(
        #     "SELECT COUNT(*) from unread_message "
        #     "left join messages on unread_message.message_id = messages.id "
        #     "where user_id = :user_id and receiver_id = :user_id and sender_id = :sender_id "
        #     "and messages.'group' = 0")
        # stmt = stmt.bindparams(user_id=user_id, sender_id=sender_id)
        # return session.execute(stmt).first()[0]
    except Exception as e:
        print(e)
        return 0
    finally:
        session.close()


def get_number_of_unread_message_group(user_id: int, group_id: int) -> int:
    session: Session = DB_Session()

    try:
        return session.query(func.count(unread_message_table.c.message_id)) \
            .join(Message, Message.id == unread_message_table.c.message_id, isouter=True) \
            .filter(unread_message_table.c.user_id == user_id, Message.receiver_id == group_id, Message.group == True)\
            .first()[0]

        # stmt = text(
        #     "SELECT COUNT(*) from unread_message "
        #     "left join messages on unread_message.message_id = messages.id "
        #     "where unread_message.user_id = :user_id and messages.receiver_id = :group_id "
        #     "and messages.group = true")
        # stmt = stmt.bindparams(user_id=user_id, group_id=group_id)
        # return session.execute(stmt)
    except:
        return 0
    finally:
        session.close()
