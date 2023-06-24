from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from bot import BotDB
from dispatcher import dp, bot


state: dict = {
    'create_meetup': False
}

# States
class CreateMeetup(StatesGroup):
    name = State()  # Will be represented in storage as 'Form:name'

@dp.message_handler(commands=['start_organizer'])
async def organizer_start_cmd_handler(message: Message):
    # if (not BotDB.user_exists(message.from_user.id)):
    #     BotDB.add_user(message.from_user.id)
    button1: InlineKeyboardButton = InlineKeyboardButton(
        text='Начать/Завершить мероприятие',
        callback_data='start_stop_meeting')
    button2: InlineKeyboardButton = InlineKeyboardButton(
        text='Добавить докладчиков',
        callback_data='add_speaker'
    )
    button3: InlineKeyboardButton = InlineKeyboardButton(
        text='Изменить программу выступления',
        callback_data='change_program'
    )

    markup_organizer_start = InlineKeyboardMarkup(inline_keyboard=[
        [button1], [button2], [button3]
    ]
    )

    await message.answer(
        f"Доброго времени суток {message.from_user.full_name} :) \nЯ - МитапБот️, бот который может управлять митапами.\nЧего желаешь хозяин?"
        , reply_markup=markup_organizer_start)


@dp.callback_query_handler(Text(equals='start_stop_meeting'))
async def organizer_start_stop_meeting(query: CallbackQuery):
    button_yes: InlineKeyboardButton = InlineKeyboardButton(text='Да', )
    button_no: InlineKeyboardButton = InlineKeyboardButton(text='Нет')

    markup_organizer_yes_no = InlineKeyboardMarkup(inline_keyboard=
                                                   [[button_yes, button_no]]
                                                   )

    active_meetups = BotDB.get_active_meetups()
    if active_meetups:
        await query.message.reply("Завершить текущее мероприятие?", reply_markup=markup_organizer_yes_no)
        await bot.send_message(query.id, text="ddd", reply_markup=markup_organizer_yes_no)
    else:
        await CreateMeetup.name.set()
        await query.message.answer(text="Нет активных митапов. \nВведи название нового мероприятия:")
    await query.answer()

@dp.message_handler(state=CreateMeetup.name)
async def organizer_create_meetup(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await state.finish()
    BotDB.add_new_meetup(message.text)
    await message.answer(text=f"Создано новое мероприятие {message.text}")

