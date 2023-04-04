from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from bot.models import User, Setting
from bot.services.db_session import db_session
from bot.data.config import get_admins


class IsPrivate(BoundFilter):
    async def check(self, message):
        if 'id' in message:
            return message.message.chat.type == types.ChatType.PRIVATE
        else:
            return message.chat.type == types.ChatType.PRIVATE


class IsPowerOff(BoundFilter):
    async def check(self, message: types.Message):
        power = db_session.query(Setting).get('power').value

        return power == "off"


class IsNotStarted(BoundFilter):
    async def check(self, message: types.Message):
        if db_session.query(User).get(message.from_user.id) is None:
            return True

        return False
    
class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        if message.from_user.id in get_admins():
            return True
        
        return False
