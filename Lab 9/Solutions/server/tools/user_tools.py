from sqlalchemy.orm.session import Session
from datebase import DB_Session, User


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
