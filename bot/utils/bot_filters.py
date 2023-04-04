from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

class IsPrivate(BoundFilter):
    async def check(self, message):
        if 'id' in message:
            return message.message.chat.type == types.ChatType.PRIVATE
        else:
            return message.chat.type == types.ChatType.PRIVATE
