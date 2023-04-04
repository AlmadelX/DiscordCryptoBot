from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot.data.loader import dp
from bot.keyboards.start import menu
from bot.services.db_session import db_session
from bot.utils.bot_filters import IsPowerOff


@dp.message_handler(IsPowerOff(), state='*')
async def filter_power_off(message: Message, state: FSMContext):
    await state.finish()

    await message.answer('Bot is powered off.')


@dp.message_handler(commands=['start', 'help'], state='*')
async def start(message: Message, state: FSMContext):
    await state.finish()

    await message.answer('Menu', reply_markup=menu(message.from_user.id))
