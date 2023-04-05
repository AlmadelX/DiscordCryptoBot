from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot.data.loader import dp
from bot.data.texts import load_button
from bot.filters import IsAdmin
from bot.keyboards import admin_menu, back_menu, start_menu
from bot.services.database import db_session
from bot.states import AddServer, DeleteServer
from bot.models import Server, Subscription
from bot.services.discord import get_last_message_id


@dp.message_handler(IsAdmin(), text=load_button('admin_btn'), state=None)
async def admin(message: Message):
    await message.reply('Admin panel:', reply_markup=admin_menu())


@dp.message_handler(IsAdmin(), text=['Back', 'Назад'], state='*')
async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.reply('Canceled', reply_markup=start_menu(message.from_user.id))


@dp.message_handler(IsAdmin(), text='Add server', state=None)
async def add_server(message: Message):
    await AddServer.name.set()
    await message.reply('Enter server name:', reply_markup=back_menu(message.from_user.id))


@dp.message_handler(IsAdmin(), state=AddServer.name)
async def add_name(message: Message, state: FSMContext):
    name = message.text

    if db_session.query(Server).filter_by(name=name).first() is not None:
        await message.reply('Server already added')
        return

    async with state.proxy() as data:
        data['name'] = name

    await AddServer.next()
    await message.reply('Enter channel link:')


@dp.message_handler(IsAdmin(), state=AddServer.link)
async def add_link(message: Message, state: FSMContext):
    link = message.text
    channel = link.split('/')[-1]

    if db_session.query(Server).filter_by(channel=channel).first() is not None:
        await message.reply('Server already added')
        return

    last_message = get_last_message_id(channel)
    if last_message == 'error':
        await message.reply('Wrong link')
        return

    async with state.proxy() as data:
        db_session.add(
            Server(name=data['name'], channel=channel, last_message=last_message))
        db_session.commit()

    await state.finish()
    await message.reply('Server added successfully', reply_markup=start_menu(message.from_user.id))


@dp.message_handler(IsAdmin(), text='Delete server', state=None)
async def delete_server(message: Message):
    await DeleteServer.name.set()
    await message.reply('Enter server name:', reply_markup=back_menu(message.from_user.id))


@dp.message_handler(IsAdmin(), state=DeleteServer.name)
async def delete_name(message: Message, state: FSMContext):
    name = message.text

    server = db_session.query(Server).filter_by(name=name).first()
    if server is None:
        await message.reply('Server not found')
        return

    db_session.query(Subscription).filter_by(server_id=server.id).delete()
    db_session.delete(server)
    db_session.commit()

    await state.finish()
    await message.reply('Server deleted successfully', reply_markup=start_menu(message.from_user.id))


@dp.message_handler(IsAdmin(), text='Get my ID', state=None)
async def get_id(message: Message):
    await message.reply(message.from_user.id, reply_markup=start_menu(message.from_user.id))
