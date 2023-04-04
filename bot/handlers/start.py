from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot.data.loader import dp
from bot.keyboards import start_menu, language_menu
from bot.models import Language, Message
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

    id = message.from_user.id

    if db_session.query(Language).get(id) is None:
        await ChooseLanguage.choose_language.set()

        welcome = db_session.query(Message).get('welcome')

        await message.reply(welcome.eng, reply_markup=language_menu())
    else:
        await message.reply('menu', reply_markup=start_menu(id))
