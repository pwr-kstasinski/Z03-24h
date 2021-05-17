from datebase import Group, DB_Session, group_members_table, User
from sqlalchemy.orm.session import Session


def get_groups() -> [Group]:
    session: Session = DB_Session()

    try:
        return session.query(Group).all()
    except:
        return []
    finally:
        session.close()


def add_group(group: Group) -> bool:
    session: Session = DB_Session()
    try:
        user = session.query(User).filter_by(id=group.owner_id).one()
        group.members.append(user)
        session.add(group)
        session.commit()
    except:
        session.rollback()
        return False
    finally:
        session.close()
    return True


def add_member(group_id: int, user_id: int) -> bool:
    session: Session = DB_Session()
    try:
        statement = group_members_table.insert().values(group_id=group_id, user_id=user_id)
        session.execute(statement)
        session.commit()
    except:
        session.rollback()
        return False
    finally:
        session.close()
    return True
