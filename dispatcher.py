import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Enable logging
logger = logging.getLogger(__name__)


# prerequisites
load_dotenv()
telegram_token = os.environ["TELEGRAM_TOKEN"]

# init
bot: Bot = Bot(token=telegram_token, parse_mode="HTML")
storage = MemoryStorage()
dp: Dispatcher = Dispatcher(bot, storage=storage)