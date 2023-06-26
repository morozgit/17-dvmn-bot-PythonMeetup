import sqlalchemy.exc
from sqlalchemy import and_

from database.main import Database
from database.methods.get import get_user_by_telegram_id, get_current_meetup
from database.models import User, Session, Meetup, Question, Lecture


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


def add_question(speaker_id: int, question: str, is_private=0):
    current_speaker = get_user_by_telegram_id(speaker_id)
    if current_speaker:
        session = Database().session
        session.add(Question(speaker_id=speaker_id, question=question, is_private=is_private))
        session.commit()


def create_meetup(name: str):
    session = Database().session
    try:
        session.query(Meetup).filter(Meetup.is_active == 1).one()
    except sqlalchemy.exc.NoResultFound:
        session.add(Meetup(name=name, is_active=1))
        session.commit()


def create_lecture(speaker_id: int, name: str):
    session = Database().session
    try:

        session.query(Lecture).filter(and_(Lecture.name.like(name), Lecture.speaker_id == speaker_id)).one()
    except sqlalchemy.exc.NoResultFound:
        meetup = get_current_meetup()
        user = get_user_by_telegram_id(speaker_id)
        session.add(Lecture(name=name, speaker_id=user.id, meetup_id=meetup.id, is_active=1))
        session.commit()
