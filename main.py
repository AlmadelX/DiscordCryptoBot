from aiogram import Dispatcher, executor

from bot.bot import scheduler
from bot.handlers import dispatcher
from bot.filters import Private
from bot.resources.database import db_session
from bot.services.discord import poll_announcements, check_token
from bot.resources.logging import logger


async def on_startup(dp: Dispatcher):
    if not check_token():
        logger.error('Invalid Discord token')
        exit(-1)

    await dp.bot.delete_webhook()
    await dp.bot.get_updates(offset=-1)

    scheduler.add_job(poll_announcements, 'interval', minutes=1)
    logger.warning('Bot started')


async def on_shutdown(dp: Dispatcher):
    logger.warning('Bot finished')
    db_session.close()

    await dp.storage.close()
    await dp.storage.wait_closed()
    await (await dp.bot.get_session()).close()


if __name__ == '__main__':
    scheduler.start()
    dispatcher.filters_factory.bind(Private)
    executor.start_polling(dispatcher, on_startup=on_startup, on_shutdown=on_shutdown)
