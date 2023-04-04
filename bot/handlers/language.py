from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot.data.loader import dp
from bot.data.texts import load_text
from bot.keyboards import languages, start_menu
from bot.models import User, Text
from bot.services.db_session import db_session
from bot.states import ChooseLanguage

@dp.message_handler(lambda message: message.text in languages, state=ChooseLanguage.choose_language)
async def valid_language(message: Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text == 'English':
        db_session.add(User(id=user_id, lang='eng'))
    elif message.text == 'Русский':
        db_session.add(User(id=user_id, lang='rus'))
    db_session.commit()
    
    reply = load_text('language_changed', user_id)

    await state.finish()
    await message.reply(reply, reply_markup=start_menu(user_id))

@dp.message_handler(state=ChooseLanguage.choose_language)
async def invalid_language(message: Message):
    await message.reply('Language not supported!')
