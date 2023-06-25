import sqlalchemy.exc

from database.main import Database
from database.methods.get import get_current_speaker, get_user_by_telegram_id
from database.models import User, Session, Meetup, Question


def create_user(telegram_id: int) -> None:
    session = Database().session
    try:
        session.query(User.telegram_id).filter(User.telegram_id == telegram_id).one()
    except sqlalchemy.exc.NoResultFound:
        session.add(User(telegram_id=telegram_id))
        session.commit()


def create_session(user: User, user_bot_session: str) -> None:
    session = Database().session
    session.add(Session(user_id=user.id, string=user_bot_session))
    session.commit()


def add_question(speaker_id: int, question: str, is_private = 0):
    current_speaker = get_user_by_telegram_id(speaker_id)
    if current_speaker:
        session = Database().session
        session.add(Question(speaker_id=speaker_id, question=question, is_private=is_private))
        session.commit()

