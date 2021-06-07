from sqlalchemy.orm.session import Session
from datebase import DB_Session, User, Group


def get_users() -> [User]:
    session: Session = DB_Session()

    try:
        return session.query(User).all()
    except:
        return []
    finally:
        session.close()


def get_user_by_name(name: str) -> User:
    session: Session = DB_Session()
    try:
        return session.query(User).filter_by(login=name).first()
    except:
        return None
    finally:
        session.close()


def get_user_by_id(id: str) -> User:
    session: Session = DB_Session()
    try:
        return session.query(User).filter_by(id=id).first()
    except:
        return None
    finally:
        session.close()


def get_user_groups(user_id: int) -> [Group]:
    session: Session = DB_Session()
    try:
        return session.query(User).filter_by(id=user_id).first().groups
    except Exception as e:
        return []
    finally:
        session.close()
