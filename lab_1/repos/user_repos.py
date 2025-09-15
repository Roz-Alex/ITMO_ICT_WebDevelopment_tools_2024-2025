from sqlmodel import select, Session

from lab_1.model.models.models import User
from lab_1.db.connection import engine


def select_all_users():
    with Session(engine) as session:
        statement = select(User)
        res = session.exec(statement).all()
        return res


def find_user(email: str):
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()
