from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot.bot import dispatcher
from bot.keyboards import start_menu
from bot.models import Server, Subscription, User
from bot.resources.database import db_session
from bot.filters import NotStarted


@dispatcher.message_handler(NotStarted(), state=None)
async def filter_not_started(message: Message):
    user_id = message.from_user.id

    db_session.add(User(id=user_id, username='@' + message.from_user.username))
    db_session.commit()

    await message.reply('Бот, который отслеживает анонсы крипто проектов.\n'
                        'Подписывайтесь на наш канал: @block_side\n'
                        'Меню бота:',
                        reply_markup=start_menu(user_id))


@dispatcher.message_handler(commands='start', state='*')
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id

    await state.finish()
    await message.reply('Бот, который отслеживает анонсы крипто проектов.\n'
                        'Подписывайтесь на наш канал: @block_side\n'
                        'Меню бота:',
                        reply_markup=start_menu(user_id))


@dispatcher.message_handler(text='📝 Доступные серверы', state=None)
async def servers(message: Message):
    server_names = [server.name for server in db_session.query(Server).all()]
    reply = 'Доступные серверы:\n' + '\n'.join(server_names)
    await message.reply(reply)


@dispatcher.message_handler(text='📚 Мои подписки', state=None)
async def subscriptions(message: Message):
    user_id = message.from_user.id
    ids = [subscription.server_id for subscription in db_session.query(
        Subscription).filter_by(user_id=message.from_user.id).all()]
    servers = db_session.query(Server).filter(Server.id.in_(ids)).all()
    names = [server.name for server in servers]

    reply = ''
    if len(names) > 0:
        reply = 'Ваши подписки:\n' + '\n'.join(names)
    else:
        reply = 'Вы не подписаны ни на один канал'

    await message.reply(reply)


@dispatcher.message_handler(text='Узнать мой ID', state=None)
async def get_my_id(message: Message):
    await message.reply(message.from_user.id, reply_markup=start_menu(message.from_user.id))
