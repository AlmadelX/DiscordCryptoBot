from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import BoundFilter

from bot.resources.config import config
from bot.models import User
from bot.resources.database import db_session


class Admin(BoundFilter):
    async def check(self, message: Message):
        return message.from_user.id in config.bot_admins


class NotStarted(BoundFilter):
    async def check(self, message: Message):
        return db_session.query(User).get(message.from_user.id) is None


class Private(BoundFilter):
    async def check(self, message):
        if 'id' in message:
            return message.message.chat.type == ChatType.PRIVATE
        else:
            return message.chat.type == ChatType.PRIVATE
