from aiogram import Bot
from aiogram.types import Message

from database.methods.create import create_user
from database.methods.get import get_user_by_telegram_id
from database.methods.update import set_org, set_speaker, set_listner
from dispatcher import dp


# @dp.message_handler(state=None, content_types=['text'])
# async def other_messages(message: Message) -> None:
#     if not get_user_by_telegram_id(message.from_user.id):
#         create_user(message.from_user.id)
#
#     await message.answer("Я вас не понял, напишите /start!")
#

@dp.message_handler(commands=['id'])
async def __get_id(msg: Message) -> None:
    bot: Bot = msg.bot
    user = msg.from_user
    await bot.send_message(user.id, f"{user.username}: {user.id}")


@dp.message_handler(commands=['set_me_org'])
async def set_me_org(msg: Message) -> None:
    bot: Bot = msg.bot
    user = msg.from_user
    set_org(user.id)
    await bot.send_message(user.id, f"is org now! {user.username}: {user.id}")


@dp.message_handler(commands=['set_me_speaker'])
async def set_me_speaker(msg: Message) -> None:
    bot: Bot = msg.bot
    user = msg.from_user
    set_speaker(user.id)
    await bot.send_message(user.id, f"is speaker now! {user.username}: {user.id}")


@dp.message_handler(commands=['set_me_listner'])
async def set_me_listner(msg: Message) -> None:
    bot: Bot = msg.bot
    user = msg.from_user
    set_listner(user.id)
    await bot.send_message(user.id, f"is listner now! {user.username}: {user.id}")
