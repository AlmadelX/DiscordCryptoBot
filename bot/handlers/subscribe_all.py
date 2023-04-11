from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot.bot import dispatcher
from bot.keyboards import confirm_menu, start_menu
from bot.models import Server, Subscription
from bot.resources.database import db_session
from bot.states import SubscribeAll


@dispatcher.message_handler(text='📣 Подписаться на всё', state=None)
async def subscribe(message: Message, state: FSMContext):
    user_id = message.from_user.id

    servers = [server.name for server in db_session.query(Server).all()]
    reply = 'Вы уверены, что хотите подписаться на эти серверы?\n' + '\n'.join(servers)
    async with state.proxy() as data:
        data['servers'] = servers

    await SubscribeAll.confirm.set()
    await message.reply(reply, reply_markup=confirm_menu())


@dispatcher.message_handler(text='Да', state=SubscribeAll.confirm)
async def proceed(message: Message, state: FSMContext):
    user_id = message.from_user.id

    async with state.proxy() as data:
        servers = db_session.query(Server).filter(
            Server.name.in_(data['servers'])).all()

        for server in servers:
            if db_session.query(Subscription).filter_by(user_id=user_id, server_id=server.id).first() is None:
                db_session.add(Subscription(
                    user_id=user_id, server_id=server.id))
        db_session.commit()

    await state.finish()
    await message.reply('Вы успешно подписались', reply_markup=start_menu(user_id))


@dispatcher.message_handler(state=SubscribeAll.confirm)
async def cancel(message: Message, state: FSMContext):
    user_id = message.from_user.id

    await state.finish()
    await message.reply('Отменено', reply_markup=start_menu(user_id))
