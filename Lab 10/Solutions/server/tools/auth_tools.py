from flask_bcrypt import Bcrypt
from sqlalchemy.orm.session import Session
from datebase import User, DB_Session

bcrypt: Bcrypt


def init_bcrypt(app):
    global bcrypt
    bcrypt = Bcrypt(app)


def check_login(user: User) -> bool:
    session: Session = DB_Session()
    try:
        db_user: User = session.query(User).filter(User.login == user.login).first()
    except:
        return False
    finally:
        session.close()

    if not db_user:
        return False
    return bcrypt.check_password_hash(db_user.password, user.password)


def is_login_free(user: User) -> bool:
    session = DB_Session()
    try:
        db_user: User = session.query(User).filter(User.login == user.login).first()
    except:
        return False
    finally:
        session.close()
    return not db_user


def register_user(user: User) -> bool:
    session = DB_Session()
    user.password = bcrypt.generate_password_hash(user.password, 10)
    try:
        session.add(user)
        session.commit()
    except:
        session.rollback()
        return False
    finally:
        session.close()
    return True
