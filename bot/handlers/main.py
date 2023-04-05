from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot.data.loader import dp
from bot.data.texts import load_text, load_button
from bot.keyboards import start_menu, language_menu
from bot.models import Text, Server, Subscription
from bot.services.database import db_session
from bot.states import Language
from bot.filters import IsPowerOff, IsNotStarted


@dp.message_handler(IsPowerOff(), state='*')
async def filter_power_off(message: Message):
    await message.reply('Bot is powered off.')


@dp.message_handler(IsNotStarted(), state=None)
async def filter_not_started(message: Message):
    reply = db_session.query(Text).get('welcome').eng

    await Language.choose.set()
    await message.reply(reply, reply_markup=language_menu())


@dp.message_handler(commands='start', state='*')
async def start(message: Message, state: FSMContext):
    await state.finish()

    user_id = message.from_user.id
    await message.reply(load_text('menu', user_id), reply_markup=start_menu(user_id))


@dp.message_handler(text=load_button('servers_btn'), state=None)
async def servers(message: Message):
    servers = [server.name for server in db_session.query(Server).all()]

    reply = '{}:\n{}'.format(
        load_text('servers_btn', message.from_user.id),
        '\n'.join(servers)
    )

    await message.reply(reply)


@dp.message_handler(text=load_button('subscriptions_btn'), state=None)
async def subscriptions(message: Message):
    user_id = message.from_user.id
    ids = [subscription.server_id for subscription in db_session.query(
        Subscription).filter_by(user_id=message.from_user.id).all()]
    servers = db_session.query(Server).filter(Server.id.in_(ids)).all()
    names = [server.name for server in servers]

    reply = ''
    if len(names) > 0:
        reply = load_text('subscriptions', user_id) + '\n'.join(names)
    else:
        reply = load_text('subscriptions_empty', user_id)

    await message.reply(reply)


@dp.message_handler(text='Get my ID', state=None)
async def get_id(message: Message):
    await message.reply(message.from_user.id, reply_markup=start_menu(message.from_user.id))
