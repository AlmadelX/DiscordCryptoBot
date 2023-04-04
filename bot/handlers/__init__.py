from .main import dp
from .subscribe_all import dp
from .subscribe import dp
from .unsubscribe import dp
from .language import dp

from bot.data.texts import load_text


@dp.message_handler(state='*')
async def fallback(message):
    await message.reply(load_text('fallback', message.from_user.id))

__all__ = ['dp']
