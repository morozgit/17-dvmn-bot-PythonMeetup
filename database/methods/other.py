from sqlalchemy import exc, and_

from database.main import Database
from database.methods.create import create_user
from database.models import User


def is_admin(telegram_id: int) -> bool:
    try:
        return bool(Database().session.query(User.admin).filter(User.telegram_id == telegram_id).one()[0])
    except exc.NoResultFound:
        create_user(telegram_id)
        return False


def is_org(telegram_id: int) -> bool:
    try:
        return bool(Database().session.query(User.organizer).filter(User.telegram_id == telegram_id).one()[0])
    except exc.NoResultFound:
        create_user(telegram_id)
        return False


def is_speaker(telegram_id: int) -> bool:
    try:
        return bool(Database().session.query(User.speaker).filter(User.telegram_id == telegram_id).one()[0])
    except exc.NoResultFound:
        create_user(telegram_id)
        return False


def is_listner(telegram_id: int) -> bool:
    try:
        user = Database().session.query(User).filter(and_(User.telegram_id == telegram_id, User.organizer == 0,
                                                          User.speaker == 0)).one()

        return bool(None != user)
    except exc.NoResultFound:
        create_user(telegram_id)
        return False
