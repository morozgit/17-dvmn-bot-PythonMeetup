from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from dispatcher import dp, bot
import aiogram.utils.markdown as fmt
from database.methods.get import get_user_by_telegram_id, get_meetup_program, get_current_speaker
from database.methods.create import create_user, add_question
from filters.main import IsSpeaker


@dp.message_handler(IsSpeaker(), commands="start_speaker")
async def speaker_start_cmd_start(message: types.Message):
    if not get_user_by_telegram_id(message.from_user.id):
        create_user(message.from_user.id)
    button_registration = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Подтвердить регистрацию', request_contact=True))
    await message.answer("Добрый день. Пройдите регистрацию", reply_markup=button_registration)


@dp.message_handler(IsSpeaker(), content_types=['contact'])
async def registration_speaker(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Начать доклад")],
        [types.KeyboardButton(text="Закончить доклад")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, )
    await message.answer("Спасибо) Регистрация пройдена", reply_markup=keyboard)


@dp.message_handler(IsSpeaker(), Text(equals="Начать доклад"))
async def start_speech(message: types.Message):
    await message.answer('Выступает {0} {1}'.format(message.from_user.first_name, message.from_user.last_name))


@dp.message_handler(IsSpeaker(), Text(equals="Закончить доклад"))
async def end_speech(message: types.Message):
    await message.answer('Доклад закончен')


@dp.message_handler(IsSpeaker())
async def get_user_question(message: types.Message):
    answer_good = InlineKeyboardButton(text='✅', callback_data='✅')
    keyboard = InlineKeyboardMarkup().row(answer_good)
    await message.reply('Вопрос от слушателя', reply_markup=keyboard)


@dp.callback_query_handler(Text(equals='✅'))
async def push_answer_good(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(fmt.text(fmt.hstrikethrough(callback_query.message.text)))
