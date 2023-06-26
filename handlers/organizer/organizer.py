from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ReplyKeyboardRemove

from database.methods.create import create_meetup, create_lecture
from database.methods.get import get_current_meetup, get_meetup_program, get_user_by_id
from database.methods.update import set_current_meetup_state, set_speaker
from dispatcher import dp
from filters.main import IsOrg


# States
class CreateMeetup(StatesGroup):
    name = State()  # Will be represented in storage as 'Form:name'


class AddLecture(StatesGroup):
    speaker = State()
    name = State()


@dp.message_handler(IsOrg(), commands=['start'])
async def organizer_start_cmd_handler(message: Message):
    button1: InlineKeyboardButton = InlineKeyboardButton(
        text='Начать/Завершить мероприятие',
        callback_data='__start_stop_meeting')
    button2: InlineKeyboardButton = InlineKeyboardButton(
        text='Добавить докладчиков',
        callback_data='__add_speaker'
    )
    button3: InlineKeyboardButton = InlineKeyboardButton(
        text='Изменить программу выступления',
        callback_data='__change_program'
    )

    markup_organizer_start = InlineKeyboardMarkup(inline_keyboard=[
        [button1], [button2], [button3]
    ]
    )

    await message.answer(
        f"Доброго времени суток {message.from_user.full_name} :) \nЯ - МитапБот️, бот который может управлять митапами.\nЧего желаешь хозяин?"
        , reply_markup=markup_organizer_start)


@dp.callback_query_handler(IsOrg(), Text(equals='__start_stop_meeting'))
async def organizer_start_stop_meeting(query: CallbackQuery):
    button_yes: InlineKeyboardButton = InlineKeyboardButton(text='Да', callback_data='end_current_meetup')
    button_no: InlineKeyboardButton = InlineKeyboardButton(text='Нет', callback_data='cancel_end_current_meetup')

    markup_organizer_yes_no = InlineKeyboardMarkup(inline_keyboard=
                                                   [[button_yes, button_no]]
                                                   )

    active_meetups = get_current_meetup()
    if active_meetups:
        await query.message.reply("Завершить текущее мероприятие?", reply_markup=markup_organizer_yes_no)
    else:
        await CreateMeetup.name.set()
        await query.message.answer(text="Нет активных митапов. \nВведи название нового мероприятия:")
    await query.answer()


@dp.callback_query_handler(IsOrg(), Text(equals='end_current_meetup'))
async def end_current_meetup(query: CallbackQuery):
    set_current_meetup_state(0)
    await query.message.delete()
    await query.message.answer(text="Текущее мероприятие завершено")
    await query.answer()


@dp.callback_query_handler(IsOrg(), Text(equals='cancel_end_current_meetup'))
async def end_current_meetup(query: CallbackQuery):
    await query.message.delete()
    await query.answer()


@dp.callback_query_handler(IsOrg(), Text(equals='__add_speaker'))
async def end_current_meetup(query: CallbackQuery):
    await query.message.answer(
        text="Для добавления докладчика необходимо выполнить команду /add_speaker telegram_user")
    await query.message.answer(
        text="т.к на данный момент телеграмм не дает возможности получить АПИ ключ, то приходится передавать ID")

    await query.answer()


@dp.message_handler(IsOrg(), commands=['add_speaker'])
async def add_speaker(message: Message):
    speaker_id = message.get_args()
    member = await dp.bot.get_chat_member(message.chat.id, speaker_id)
    if not member:
        await message.reply(f"Участник с данным ID: {speaker_id} не состоит в чате бота")
        return
    set_speaker(speaker_id)

    await message.answer(f"Пользователь с ID: {speaker_id} сделан докладчиком")
    await message.bot.send_message(
        speaker_id,
        f"Организатор @{message.from_user.username} сделал Вас докладчиком!",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.callback_query_handler(IsOrg(), Text(equals='__change_program'))
async def end_current_meetup(query: CallbackQuery):
    message = query.message
    program = get_meetup_program()
    if len(program):
        await message.answer(
            "Программа мероприятия:"
        )
        for meetup in program:
            member = await dp.bot.get_chat_member(message.chat.id, meetup.speaker_id)

            await message.answer(
                f"Докладчик: {member.user.full_name} Тема: {meetup.theme}"
            )
    else:
        await message.answer(
            """Программа мероприятия еще не сформирована
            для добавления доклада воспользуйтесь командой /add_lecture
            """
        )

    await query.answer()


@dp.message_handler(IsOrg(), commands=["view_program"])
async def organizer_view_program(message: Message):
    program = get_meetup_program()
    if len(program):
        await message.answer(
            "Программа мероприятия:"
        )
        for lecture in program:
            speaker = get_user_by_id(lecture.speaker_id)
            member = await dp.bot.get_chat_member(message.chat.id, speaker.telegram_id)

            await message.answer(
                f"Докладчик: @{member.user.username} Тема: {lecture.name}"
            )
    else:
        await message.answer(
            """Программа мероприятия еще не сформирована
            для добавления доклада воспользуйтесь командой /add_lecture
            """
        )


@dp.message_handler(IsOrg(), commands=["add_lecture"])
async def organizer_add_lecture(message: Message):
    await AddLecture.speaker.set()
    await message.answer(
        """Введите telegram_id докладчика
        """
    )


@dp.message_handler(IsOrg(), state=AddLecture.speaker)
async def organizer_add_lecture_speaker(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['speaker'] = message.text

    await AddLecture.next()
    await message.reply("Укажите название лекции:")


@dp.message_handler(IsOrg(), state=AddLecture.name)
async def organizer_add_lecture_speaker(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    active_meetups = get_current_meetup()
    if active_meetups:
        create_lecture(data['speaker'], data['name'])
        await state.finish()
        await message.reply("Спасибо. /view_program")
        return

    message.answer("Сейчас нет активных митапов")


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(IsOrg(), state=CreateMeetup.name)
async def organizer_create_meetup(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await state.finish()
    create_meetup(message.text)
    await message.answer(text=f"Создано новое мероприятие {message.text}")
