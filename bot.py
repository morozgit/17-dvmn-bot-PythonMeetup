from contextlib import suppress

from aiogram import Dispatcher
from aiogram.utils import executor

from database import register_models
from database.methods.get import get_users_with_sessions
from db import BotDB
from dispatcher import dp, bot
import handlers
from filters import register_all_filters


async def __on_start_up(dp: Dispatcher) -> None:
    register_models()
    register_all_filters(dp)

    # users = get_users_with_sessions()
    # count = 0
    #
    # if not users:
    #     return

    # for user in users:
    #     with suppress(ChatNotFound, BotBlocked):
    #         if user.session.enable:
    #             start_process_if_sessions_exists(user.telegram_id)
    #         await dp.bot.send_message(user.telegram_id, "Бот обновлен!",
    #                                   reply_markup=get_main_keyboard(user.telegram_id))
    #         count += 1


def main():
    """Start the bot."""
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)


if __name__ == "__main__":
    main()
