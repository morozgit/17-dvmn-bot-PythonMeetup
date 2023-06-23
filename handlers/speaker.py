from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from dispatcher import dp, bot
from db import BotDB


bd = BotDB

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    button_registration = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Подтвердить регистрацию', request_contact=True))
    await message.answer("Добрый день. Пройдите регистрацию", reply_markup=button_registration)

@dp.message_handler(content_types=['contact'])
async def registration_speaker(message: types.Message):
    print(message.from_id)
    keyboard = types.ReplyKeyboardRemove()
    await message.answer("Спасибо) Регистрация пройдена", reply_markup=keyboard)

# @dp.message_handler(state=but)
# async def speak_start(message: types.Message):
#     print("start")
#     keyboard = types.InlineKeyboardMarkup()
#     keyboard.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="random_value"))
#     await message.answer("Нажмите на кнопку, чтобы бот отправил число от 1 до 10", reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp)