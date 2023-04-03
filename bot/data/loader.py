from aiogram import Bot, Dispatcher

from bot.data.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
