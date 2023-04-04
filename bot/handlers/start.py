from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot.data.loader import dp
from bot.data.texts import load_text
from bot.keyboards import start_menu, language_menu
from bot.models import Language, Text
from bot.services.db_session import db_session
from bot.states import ChooseLanguage
from bot.filters import IsPowerOff


@dp.message_handler(IsPowerOff(), state='*')
async def filter_power_off(message: Message, state: FSMContext):
    await state.finish()

    await message.reply('Bot is powered off.')


@dp.message_handler(commands='start', state='*')
async def start(message: Message, state: FSMContext):
    await state.finish()

    user_id = message.from_user.id

    if db_session.query(Language).get(user_id) is None:
        reply = db_session.query(Text).get('welcome').eng

        await ChooseLanguage.choose_language.set()
        await message.reply(reply, reply_markup=language_menu())
    else:
        reply = load_text('menu', user_id)
        await message.reply(reply, reply_markup=start_menu(id))
