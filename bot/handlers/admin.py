from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot.bot import dispatcher
from bot.filters import Admin
from bot.keyboards import admin_menu, append_menu, back_menu, start_menu
from bot.models import Channel, Server, Subscription, User
from bot.resources.database import db_session
from bot.services.discord import get_last_message_id
from bot.states import AddServer, DeleteServer, Mailing
from bot.notifier import notify_all


@dispatcher.message_handler(Admin(), text='Админ-панель', state=None)
async def admin_panel(message: Message):
    await message.reply('Админ-панель:', reply_markup=admin_menu())


@dispatcher.message_handler(Admin(), text='Назад', state='*')
async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.reply('Отменено', reply_markup=start_menu(message.from_user.id))


@dispatcher.message_handler(Admin(), text='Добавить сервер', state=None)
async def add_server(message: Message):
    await AddServer.name.set()
    await message.reply('Введите название сервера:', reply_markup=back_menu())


@dispatcher.message_handler(Admin(), state=AddServer.name)
async def add_server(message: Message, state: FSMContext):
    name = message.text

    if db_session.query(Server).filter_by(name=name).first() is not None:
        await message.reply('Сервер уже добавлен')
        return

    async with state.proxy() as data:
        data['server'] = Server(name=name)
        data['channels'] = []

    await AddServer.next()
    await message.reply('Введите ссылку на канал:')


@dispatcher.message_handler(Admin(), text='Завершить', state=AddServer.link)
async def finish(message: Message, state: FSMContext):
    async with state.proxy() as data:
        db_session.add(data['server'])
        db_session.commit()

        for channel in data['channels']:
            db_session.add(Channel(
                id=channel[0],
                server=data['server'].id,
                last_message=channel[1]
            ))
        db_session.commit()

    await state.finish()
    await message.reply('Сервер успешно добавлен', reply_markup=start_menu(message.from_user.id))


@dispatcher.message_handler(Admin(), state=AddServer.link)
async def add_link(message: Message, state: FSMContext):
    link = message.text
    channel = link.split('/')[-1]

    if db_session.query(Channel).filter_by(id=channel).first() is not None:
        await message.reply('Канал уже добавлен')
        return

    last_message = get_last_message_id(channel)
    if last_message == 'error':
        await message.reply('Неверная ссылка')
        return

    async with state.proxy() as data:
        data['channels'].append([channel, last_message])

    await message.reply('Введите следующую ссылку:', reply_markup=append_menu())


@dispatcher.message_handler(Admin(), text='Удалить сервер', state=None)
async def delete_server(message: Message):
    await DeleteServer.name.set()
    await message.reply('Введите название сервера:', reply_markup=back_menu())


@dispatcher.message_handler(Admin(), state=DeleteServer.name)
async def delete_name(message: Message, state: FSMContext):
    name = message.text

    server = db_session.query(Server).filter_by(name=name).first()
    if server is None:
        await message.reply('Сервер не найден')
        return

    db_session.query(Channel).filter_by(server=server.id).delete()
    db_session.query(Subscription).filter_by(server_id=server.id).delete()
    db_session.delete(server)
    db_session.commit()

    await state.finish()
    await message.reply('Сервер успешно удален', reply_markup=start_menu(message.from_user.id))


@dispatcher.message_handler(Admin(), text='Пользователи', state=None)
async def users(message: Message):
    users = db_session.query(User).all()
    usernames = [user.username for user in users]
    reply = 'Пользователи бота:\n' + '\n'.join(usernames)

    await message.reply(reply, reply_markup=start_menu(message.from_user.id))


@dispatcher.message_handler(Admin(), text='Рассылка', state=None)
async def mailing_query(message: Message):
    await Mailing.input.set()
    await message.reply('Введите сообщение для рассылки:', reply_markup=back_menu())


@dispatcher.message_handler(text='Назад', state=Mailing.input)
async def mailing_cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.reply('Отменено', reply_markup=start_menu(message.from_user.id))


@dispatcher.message_handler(state=Mailing.input)
async def mailing(message: Message, state: FSMContext):
    await notify_all(message.text)

    await state.finish()
    await message.reply('Рассылка успешно завершена', reply_markup=start_menu(message.from_user.id))
