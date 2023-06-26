import aiogram.utils.markdown as fmt
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from database.main import Database
from database.models import Question
from dispatcher import bot, dp
from filters.main import IsSpeaker


class StartSpeech(StatesGroup):
    speech = State()

@dp.message_handler(IsSpeaker(), commands="start")
async def speaker_start_cmd_start(message: types.Message):
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
    start_question = InlineKeyboardButton(text='Принимать вопросы', callback_data='Принимать вопросы')
    keyboard = InlineKeyboardMarkup().row(start_question)
    await message.answer('Выступает {0} {1}'.format(message.from_user.first_name, message.from_user.last_name),
                         reply_markup=keyboard)


@dp.message_handler(IsSpeaker(), Text(equals="Закончить доклад"))
async def end_speech(message: types.Message):
    await message.answer('Доклад закончен')


@dp.callback_query_handler(Text(equals="Принимать вопросы"))
async def get_user_question(query: types.CallbackQuery):
    print('sdfsdf')
    answer_good = InlineKeyboardButton(text='✅', callback_data='✅')
    keyboard = InlineKeyboardMarkup().row(answer_good)
    question_from_user = Database().session.query(Question).filter(Question.question).all()
    print(question_from_user)
    await query.message.reply(question_from_user, reply_markup=keyboard)


@dp.callback_query_handler(Text(equals='✅'))
async def push_answer_good(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(fmt.text(fmt.hstrikethrough(callback_query.message.text)))