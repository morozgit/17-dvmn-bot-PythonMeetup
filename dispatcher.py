import logging
import os

from aiogram import Bot, Dispatcher
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
bot = Bot(token=telegram_token, parse_mode="HTML")
dp = Dispatcher(bot)