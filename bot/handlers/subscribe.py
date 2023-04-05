from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from sqlalchemy import func

from bot.data.loader import dp
from bot.data.texts import load_button, load_text
from bot.keyboards import start_menu, back_menu
from bot.models import Server, Subscription
from bot.services.database import db_session
from bot.states import Subscribe


@dp.message_handler(text=load_button('subscribe_btn'), state=None)
async def subscribe(message: Message):
    user_id = message.from_user.id
    reply = load_text('subscription_query', user_id)

    await Subscribe.input.set()
    await message.reply(reply, reply_markup=back_menu(user_id))


@dp.message_handler(state=Subscribe.input)
async def input(message: Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['Back', 'Назад']:
        reply = load_text('canceled', user_id)

        await state.finish()
        await message.reply(reply, reply_markup=start_menu(user_id))
        return

    server_name = message.text.lower()
    server = db_session.query(Server).filter(
        func.lower(Server.name) == server_name).first()
    if server is None:
        reply = load_text('server_not_supported', user_id)
        await message.reply(reply)
        return

    if db_session.query(Subscription).filter_by(user_id=user_id, server_id=server.id).first() is not None:
        reply = load_text('subscription_already', user_id)
        await message.reply(reply)
        return

    db_session.add(Subscription(user_id=user_id, server_id=server.id))
    db_session.commit()

    reply = load_text('subscription_success', user_id)

    await state.finish()
    await message.reply(reply, reply_markup=start_menu(user_id))
