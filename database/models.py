from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .main import Database


class User(Database.BASE):
    __tablename__ = 'USER'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    vip = Column(Integer, default=0)
    admin = Column(Integer, default=0)
    speaker = Column(Integer, default=0)
    organizer = Column(Integer, default=0)
    session = relationship('Session', uselist=False, backref="USER", passive_deletes=True)
    meetup = relationship('Meetup', uselist=False, backref="USER", passive_deletes=True)


class Session(Database.BASE):
    __tablename__ = 'SESSION'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('USER.id', ondelete='CASCADE'), unique=True)
    string = Column(String, nullable=False)
    enable = Column(Integer, default=0)


class Meetup(Database.BASE):
    __tablename__ = 'MEETUP'
    id: Mapped[int] = mapped_column(primary_key=True)
    speaker_id: Mapped[int] = mapped_column(ForeignKey("USER.id"))
    theme: Mapped[str]
    is_active: Mapped[int]


class Question(Database.BASE):
    __tablename__ = 'QUESTION'
    id: Mapped[int] = mapped_column(primary_key=True)
    speaker_id: Mapped[int] = mapped_column(ForeignKey("USER.id"))
    question: Mapped[str] = mapped_column(default="")
    is_private: Mapped[int] = mapped_column(default=0)
    is_answered: Mapped[int] = mapped_column(default=0)


def register_models():
    Database.BASE.metadata.create_all(Database().engine)
