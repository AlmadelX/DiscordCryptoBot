from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot.data.loader import dp
from bot.data.texts import load_text, load_button
from bot.keyboards import start_menu, language_menu
from bot.models import User, Text
from bot.services.database import db_session
from bot.states import Language


@dp.message_handler(text=load_button('language_btn'), state=None)
async def language(message: Message):
    user_id = message.from_user.id
    reply = load_text('language_query', user_id)

    await Language.choose.set()
    await message.reply(reply, reply_markup=language_menu())


@dp.message_handler(lambda message: message.text in ['English', 'Русский'], state=Language.choose)
async def valid(message: Message, state: FSMContext):
    user_id = message.from_user.id

    lang=''
    if message.text == 'English':
        lang='eng'
    elif message.text == 'Русский':
        lang='rus'
    
    user = db_session.query(User).filter_by(id=user_id).first()
    if user is None:
        db_session.add(User(id=user_id, lang=lang))
    else:
        user.lang = lang
    db_session.commit()

    reply = load_text('language_changed', user_id)

    await state.finish()
    await message.reply(reply, reply_markup=start_menu(user_id))


@dp.message_handler(state=Language.choose)
async def invalid(message: Message):
    await message.reply('Language not supported!')
