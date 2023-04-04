from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot.data.loader import dp
from bot.data.texts import load_button, load_text
from bot.keyboards import confirm_menu, start_menu, back_menu
from bot.models import Server, Subscription
from bot.services.db_session import db_session
from bot.states import Subscribe


@dp.message_handler(text=load_button('subscribe_all_btn'), state=None)
async def subscribe_all(message: Message, state: FSMContext):
    user_id = message.from_user.id

    servers = [server.name for server in db_session.query(Server).all()]
    reply = load_text('subscription_confirm', user_id) + '\n'.join(servers)
    async with state.proxy() as data:
        data['servers'] = servers

    await Subscribe.confirm_all.set()
    await message.reply(reply, reply_markup=confirm_menu(user_id))


@dp.message_handler(lambda message: message.text in ['Yes', 'Да'], state=Subscribe.confirm_all)
async def confirm_all(message: Message, state: FSMContext):
    user_id = message.from_user.id

    async with state.proxy() as data:
        servers = db_session.query(Server).filter(
            Server.name.in_(data['servers'])).all()

        for server in servers:
            if db_session.query(Subscription).filter_by(user_id=user_id, server_id=server.id).first() is None:
                db_session.add(Subscription(
                    user_id=user_id, server_id=server.id))

        db_session.commit()

    reply = load_text('subscription_success', user_id)

    await state.finish()
    await message.reply(reply, reply_markup=start_menu(user_id))


@dp.message_handler(state=Subscribe.confirm_all)
async def cancel_all(message: Message, state: FSMContext):
    user_id = message.from_user.id

    reply = load_text('canceled', user_id)

    await state.finish()
    await message.reply(reply, reply_markup=start_menu(user_id))


@dp.message_handler(text=load_button('subscribe_btn'), state=None)
async def subscribe(message: Message, state: FSMContext):
    user_id = message.from_user.id
    reply = load_text('subscription_query', user_id)

    await Subscribe.input.set()
    await message.reply(reply, reply_markup=back_menu(user_id))


@dp.message_handler(state=Subscribe.input)
async def subscribe_input(message: Message, state: FSMContext):
    user_id = message.from_user.id
    servers = db_session.query(Server).all()
    names = [server.name.lower() for server in servers]
    reply = ''

    if message.text in ['Back', 'Назад']:
        reply = load_text('canceled', user_id)

        await state.finish()
        await message.reply(reply, reply_markup=start_menu(user_id))
        return

    wanted_server = message.text.lower()
    if wanted_server in names:
        server_id = 0
        for server in servers:
            if server.name.lower() == wanted_server:
                server_id = server.id

        if db_session.query(Subscription).filter_by(user_id=user_id, server_id=server_id).first() is None:
            db_session.add(Subscription(user_id=user_id, server_id=server_id))
            reply = load_text('subscription_success', user_id)
        else:
            reply = load_text('subscription_already', user_id)

        await state.finish()
        await message.reply(reply, reply_markup=start_menu(user_id))
    else:
        reply = load_text('subscription_miss', user_id)
        await message.reply(reply)
