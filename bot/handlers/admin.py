from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot.data.loader import dp
from bot.data.texts import load_button
from bot.filters import IsAdmin


@dp.message_handler(IsAdmin(), text=load_button('admin_btn'), state=None)
async def admin(message: Message):
    await message.reply('Admin panel')
