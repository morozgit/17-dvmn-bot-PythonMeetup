from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from dispatcher import dp, bot


@dp.message_handler(commands="start_speaker")
async def speaker_start_cmd_start(message: types.Message):
    button_registration = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Подтвердить регистрацию', request_contact=True))
    await message.answer("Добрый день. Пройдите регистрацию", reply_markup=button_registration)

@dp.message_handler(content_types=['contact'])
async def registration_speaker(message: types.Message):
    print(message.from_id)
    kb = [
        [types.KeyboardButton(text="Начать доклад")],
        [types.KeyboardButton(text="Закончить доклад")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,)
    await message.answer("Спасибо) Регистрация пройдена", reply_markup=keyboard)

@dp.message_handler(Text(equals="Начать доклад"))
async def start_speech(message: types.Message):
    print('Начать доклад')
    await message.answer('Начать доклад')

@dp.message_handler(Text(equals="Закончить доклад"))
async def end_speech(message: types.Message):
    print('Закончить доклад')
    await message.answer('Закончить доклад')

@dp.message_handler()
async def get_user_question(message: types.Message):
    print('Вопрос от слушателя')
    await message.answer('Вопрос от слушателя')

