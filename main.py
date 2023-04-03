from aiogram import Dispatcher, executor

from bot.handlers import dp
from bot.utils.bot_logging import bot_logger

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
