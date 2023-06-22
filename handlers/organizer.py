from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from dispatcher import dp, bot

button1 = KeyboardButton('Начать/Завершить мероприятие')
button2 = KeyboardButton('Добавить докладчиков')
button3 = KeyboardButton('Изменить программу выступления')

markup_speaker_start = ReplyKeyboardMarkup(resize_keyboard=True).row(
    button1, button2, button3
)


@dp.message_handler(commands='start_organizer')
async def organizer_start_cmd_handler(message: types.Message):
    # if (not BotDB.user_exists(message.from_user.id)):
    #     BotDB.add_user(message.from_user.id)
    await message.answer(
        f"Доброго времяни суток {message.from_user.full_name} :) \nЯ - МитапБот️, бот который может управлять митапами.\nЧего желаешь хозяин?"
        , reply_markup=markup_speaker_start)

@dp.message_handler(Text(equals="Начать/Завершить мероприятие"))
async def speaker_with_puree(message: types.Message):
    await message.reply("Где хочешь погоду узнать")
