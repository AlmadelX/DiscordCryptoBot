from aiogram.types import Message

from .main import dispatcher
from .subscribe_all import dispatcher
from .subscribe import dispatcher
from .unsubscribe import dispatcher
from .support import dispatcher
from .admin import dispatcher


@dispatcher.message_handler(state='*')
async def fallback(message: Message):
    await message.reply('Команда не поддерживается')

__all__ = ['dispatcher']
