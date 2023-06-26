from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from database.methods.create import add_question
from database.methods.get import get_meetup_program, get_current_speaker, get_user_by_id
from dispatcher import dp
from filters.main import IsListner


# States
class SpeakerQuestion(StatesGroup):
    question = State()  # Will be represented in storage as 'Form:name'


@dp.message_handler(IsListner(), commands=['start'])
async def organizer_start_cmd_handler(message: Message):
    await message.answer(
        f"Доброго времени суток {message.from_user.full_name} :) \nЯ - МитапБот, бот который может управлять митапами.\nЧего желаешь хозяин?"
    )
    await message.answer(
        f"Доступные команды бота:\n"
        f"/show_meetup_program - показать доступные мероприятия\n"
        f"/question - отправить вопрос текущему докладчику",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message_handler(IsListner(), commands=["show_meetup_program"])
async def show_meetup_program(message: Message):
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
            "Программа мероприятия еще не сформирована"
        )


@dp.message_handler(IsListner(), commands=["question"])
async def send_question(message: Message):
    await SpeakerQuestion.question.set()
    await message.answer(
        "Напишите Ваш вопрос докладчику и отправьте сообщение.\nДля отмены отправки вопроса введите /cancel")


@dp.message_handler(IsListner(), state=SpeakerQuestion.question)
async def process_name(message: Message, state: FSMContext):
    """
    Process question
    """
    async with state.proxy() as data:
        data['question'] = message.text

    current_speaker_id = get_current_speaker()
    current_speaker_tgid = get_user_by_id(current_speaker_id).telegram_id
    add_question(current_speaker_id, data['question'])
    await state.finish()
    await message.bot.send_message(
        current_speaker_tgid,
        f"Получен вопрос от @{message.from_user.username}\n{data['question']}"
    )
    await message.reply("Спасибо! Ваш вопрос отправлен текущему докладчику!")


@dp.message_handler(IsListner(), state='*', commands='cancel')
@dp.message_handler(IsListner(), Text(equals='cancel', ignore_case=True), state='*')
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
    await message.reply('Отменено.', reply_markup=ReplyKeyboardRemove())
