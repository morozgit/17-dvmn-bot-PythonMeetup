from __future__ import annotations

from sqlalchemy import exc

from database.main import Database
from database.models import User, Session, Meetup


def get_user_by_telegram_id(telegram_id: int) -> User | None:
    try:
        return Database().session.query(User).filter(User.telegram_id == telegram_id).one()
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
    program = Database().session.query(
        Meetup
    ).where(Meetup.is_active == 1).all()

    return program

def get_current_speaker():
    try:
        current_meetup = Database().session.query(
            Meetup
        ).where(Meetup.is_active == 1).one()
        return current_meetup.speaker_id
    except exc.NoResultFound:
        return None
