from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from bot.models import Setting
from bot.services.db_session import db_session


class IsPrivate(BoundFilter):
    async def check(self, message):
        if 'id' in message:
            return message.message.chat.type == types.ChatType.PRIVATE
        else:
            return message.chat.type == types.ChatType.PRIVATE


class IsPowerOff(BoundFilter):
    async def check(self, message: types.Message):
        power = db_session.query(Setting).get('power')

        return power.value == "off"
