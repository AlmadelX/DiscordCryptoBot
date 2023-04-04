from aiogram import Dispatcher, executor

from bot.data.config import get_admins
from bot.handlers import dp
from bot.utils.bot_filters import IsPrivate
from bot.utils.bot_logging import bot_logger


async def on_startup(dp: Dispatcher):
    await dp.bot.delete_webhook()
    await dp.bot.get_updates(offset=-1)

    bot_logger.info('Bot started')

    if (len(get_admins()) == 0):
        bot_logger.error('Bot admins list is not specified in settings!')


async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()
    await (await dp.bot.get_session()).close()

if __name__ == '__main__':
    dp.filters_factory.bind(IsPrivate)
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
