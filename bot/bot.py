from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.utils.exceptions import ValidationError, Unauthorized
from bot.resources.logging import logger

from bot.resources.config import config

try:
    bot = Bot(token=config.bot_token)
except (ValidationError, Unauthorized):
    logger.critical('Invalid Telegram token')
    exit(-1)

dispatcher = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()
