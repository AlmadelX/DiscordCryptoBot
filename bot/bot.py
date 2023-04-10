from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.resources.config import config

bot = Bot(token=config.bot_token)

dispatcher = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()
