from __future__ import annotations

from sqlalchemy import exc, and_

from database.main import Database
from database.models import User, Session, Meetup, Lecture


def get_user_by_telegram_id(telegram_id: int) -> User | None:
    try:
        return Database().session.query(User).filter(User.telegram_id == telegram_id).one()
    except exc.NoResultFound:
        return None


def get_user_by_id(id: int) -> User | None:
    try:
        return Database().session.query(User).filter(User.id == id).one()
    except exc.NoResultFound:
        return None


def get_users_with_sessions() -> list[User]:
    return Database().session.query(User).filter(User.session).all()


def get_all_telegram_id() -> list[tuple[int]]:
    return Database().session.query(User.telegram_id).all()


def get_user_count() -> int:
    return Database().session.query(User).filter(User.admin == 0).count()


def get_sessions_count() -> int:
    return Database().session.query(User.session).join(User.session).where(User.admin == 0).count()


def get_sessions_enable_count(vip: bool) -> int:
    return Database().session.query(User).filter(
        User.vip == int(vip),
        User.admin == 0,
        User.session.has(Session.enable == 1)
    ).count()


def get_meetup_program():
    try:
        current_meetup = Database().session.query(
            Meetup
        ).where(Meetup.is_active == 1).one()

        program = Database().session.query(
            Lecture
        ).where(Lecture.meetup_id == current_meetup.id).all()

        return program
    except exc.NoResultFound:
        return []


def get_current_meetup():
    try:
        current_meetup = Database().session.query(
            Meetup
        ).where(Meetup.is_active == 1).one()

        return current_meetup
    except exc.NoResultFound:
        return []


def get_current_speaker():
    try:
        current_meetup = Database().session.query(
            Meetup
        ).where(Meetup.is_active == 1).one()

        current_lecture = Database().session.query(
            Lecture
        ).where(and_(Lecture.is_active == 1, Lecture.meetup_id == current_meetup.id)).one()
        return current_lecture.speaker_id
    except exc.NoResultFound:
        return None
