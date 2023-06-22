from aiogram import executor

from db import BotDB
from dispatcher import dp
import handlers

BotDB = BotDB('meetup.db')


def main():
    """Start the bot."""
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
