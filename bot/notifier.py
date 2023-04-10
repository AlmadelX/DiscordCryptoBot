import asyncio

from bot.bot import bot
from bot.models import Server, Subscription, User
from bot.resources.database import db_session


async def notify_subscribers(server_id: int, announcement: str):
    server_name = db_session.query(Server).get(server_id).name
    subscriptions = db_session.query(
        Subscription
    ).filter_by(server_id=server_id).all()

    tasks = []
    for subscription in subscriptions:
        message = 'Новый анонс от {}:\n{}'.format(
            server_name,
            announcement
        )
        tasks.append(asyncio.create_task(bot.send_message(subscription.user_id, message)))
    await asyncio.wait(tasks)


async def notify_all(message: str):
    users = db_session.query(User).all()

    tasks = []
    for user in users:
        tasks.append(asyncio.create_task(bot.send_message(user.id, message)))
    await asyncio.wait(tasks)
