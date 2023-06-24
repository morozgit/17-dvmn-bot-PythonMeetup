from aiogram import types

from bot import dp, BotDB
from handlers.organizer import organizer_start_cmd_handler
from handlers.speaker import speaker_start_cmd_start


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    if (not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)

    user_is_org = True
    user_id_speaker = False
    user_is_listener = False
    if user_is_org:
        await organizer_start_cmd_handler(message)

    if user_id_speaker:
        await speaker_start_cmd_start(message)

    if user_is_listener:
        pass

    #await message.answer(f"Привет {message.from_user.full_name}!\nРады снова видеть тебя!")
