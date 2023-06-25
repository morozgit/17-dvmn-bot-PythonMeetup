from sqlalchemy import exc

from database.main import Database
from database.models import User


def is_admin(telegram_id: int) -> bool:
    try:
        return bool(Database().session.query(User.admin).filter(User.telegram_id == telegram_id).one()[0])
    except exc.NoResultFound:
        return False


def is_org(telegram_id: int) -> bool:
    try:
        return bool(Database().session.query(User.organizer).filter(User.telegram_id == telegram_id).one()[0])
    except exc.NoResultFound:
        return False


def is_speaker(telegram_id: int) -> bool:
    try:
        return bool(Database().session.query(User.speaker).filter(User.telegram_id == telegram_id).one()[0])
    except exc.NoResultFound:
        return False
