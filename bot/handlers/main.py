from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot.data.loader import dp
from bot.data.texts import load_text
from bot.keyboards import start_menu, language_menu
from bot.models import Language, Text
from bot.services.db_session import db_session
from bot.states import ChooseLanguage
from bot.filters import IsPowerOff, IsNotStarted


@dp.message_handler(IsPowerOff(), state='*')
async def filter_power_off(message: Message):
    await message.reply('Bot is powered off.')


@dp.message_handler(IsNotStarted(), state=None)
async def filter_not_started(message: Message):
    reply = db_session.query(Text).get('welcome').eng

    await ChooseLanguage.choose_language.set()
    await message.reply(reply, reply_markup=language_menu())


@dp.message_handler(commands='start', state='*')
async def start(message: Message, state: FSMContext):
    await state.finish()

    user_id = message.from_user.id
    await message.reply(load_text('menu', user_id), reply_markup=start_menu(user_id))
