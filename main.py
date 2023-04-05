from aiogram import Dispatcher, executor

from bot.data.config import get_admins
from bot.data.loader import scheduler
from bot.handlers import dp
from bot.filters import IsPrivate
from bot.services.database import db_session
from bot.services.discord import poll_announcements
from bot.utils.bot_logging import bot_logger


async def on_startup(dp: Dispatcher):
    await dp.bot.delete_webhook()
    await dp.bot.get_updates(offset=-1)

    scheduler.add_job(poll_announcements, 'interval', minutes=1)

    bot_logger.info('Bot started')

    if (len(get_admins()) == 0):
        bot_logger.error('Bot admins list is not specified in settings!')


async def on_shutdown(dp: Dispatcher):
    db_session.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    await (await dp.bot.get_session()).close()

if __name__ == '__main__':
    scheduler.start()
    dp.filters_factory.bind(IsPrivate)
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
