from database.main import Database
from database.methods.get import get_user_by_telegram_id
from database.models import User


def set_admin(telegram_id: int) -> None:
    Database().session.query(User).filter(User.telegram_id == telegram_id).update(values={User.admin: 1})
    Database().session.commit()


def set_org(telegram_id: int) -> None:
    Database().session.query(User).filter(User.telegram_id == telegram_id).update(
        values={User.organizer: 1, User.speaker: 0})
    Database().session.commit()


def set_speaker(telegram_id: int) -> None:
    Database().session.query(User).filter(User.telegram_id == telegram_id).update(
        values={User.organizer: 0, User.speaker: 1})
    Database().session.commit()


def set_listner(telegram_id: int) -> None:
    Database().session.query(User).filter(User.telegram_id == telegram_id).update(
        values={User.organizer: 0, User.speaker: 0})
    Database().session.commit()


def update_session_status(telegram_id, enable) -> None:
    user = get_user_by_telegram_id(telegram_id)
    if user and user.session:
        user.session.enable = int(enable)
    Database().session.commit()
