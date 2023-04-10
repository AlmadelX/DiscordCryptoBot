from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from sqlalchemy import func

from bot.bot import dispatcher
from bot.keyboards import start_menu, back_menu
from bot.models import Server, Subscription
from bot.resources.database import db_session
from bot.states import Unsubscribe


@dispatcher.message_handler(text='❌ Отписаться', state=None)
async def subscribe(message: Message):
    await Unsubscribe.input.set()
    await message.reply('Введите название сервера, от которого хотите отписаться:', reply_markup=back_menu())


@dispatcher.message_handler(text='Назад', state=Unsubscribe.input)
async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.reply('Отменено', reply_markup=start_menu(message.from_user.id))


@dispatcher.message_handler(state=Unsubscribe.input)
async def query(message: Message, state: FSMContext):
    user_id = message.from_user.id

    server_name = message.text.lower()
    server = db_session.query(Server).filter(
        func.lower(Server.name) == server_name).first()
    if server is None:
        await message.reply('Сервер не поддерживается')
        return

    subscription = db_session.query(Subscription).filter_by(
        user_id=user_id, server_id=server.id).first()
    if subscription is None:
        await message.reply('Вы не подписаны на этот сервер')
        return

    db_session.delete(subscription)
    db_session.commit()

    await state.finish()
    await message.reply('Вы успешно отписались', reply_markup=start_menu(user_id))
