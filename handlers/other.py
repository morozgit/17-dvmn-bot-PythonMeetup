from aiogram import Dispatcher, Bot
from aiogram.types import Message

from database.methods.create import create_user
from database.methods.get import get_user_by_telegram_id
from dispatcher import dp


@dp.message_handler(state=None, content_types=['text'])
async def other_messages(message: Message) -> None:
    if not get_user_by_telegram_id(message.from_user.id):
        create_user(message.from_user.id)

    await message.answer("Я вас не понял, напишите /start!")


@dp.message_handler(commands=['id'])
async def __get_id(msg: Message) -> None:
    bot: Bot = msg.bot
    user = msg.from_user
    await bot.send_message(user.id, f"{user.username}: {user.id}")
