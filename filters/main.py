from aiogram import Dispatcher
from aiogram.dispatcher.filters import Filter
from aiogram.types import Message

from database.methods.other import is_admin, is_org, is_speaker, is_listner


class IsAdmin(Filter):
    key = "is_admin"

    async def check(self, message: Message) -> bool:
        return is_admin(message.from_user.id)


class IsOrg(Filter):
    key = "is_org"

    async def check(self, message: Message) -> bool:
        return is_org(message.from_user.id)


class IsSpeaker(Filter):
    key = "is_speaker"

    async def check(self, message: Message) -> bool:
        return is_speaker(message.from_user.id)

class IsListner(Filter):
    key = "is_listner"

    async def check(self, message: Message) -> bool:
        return is_listner(message.from_user.id)


class NotAdmin(Filter):
    key = "not_admin"

    async def check(self, message: Message) -> bool:
        return False if is_admin(message.from_user.id) else True


class NotOrg(Filter):
    key = "not_org"

    async def check(self, message: Message) -> bool:
        return False if is_org(message.from_user.id) else True


class NotSpeaker(Filter):
    key = "not_speaker"

    async def check(self, message: Message) -> bool:
        return False if is_speaker(message.from_user.id) else True


def register_all_filters(dp: Dispatcher):
    filters = (
        NotAdmin,
        IsAdmin,
        NotOrg,
        IsOrg,
        NotSpeaker,
        IsSpeaker
    )
    for filter in filters:
        dp.bind_filter(filter)
