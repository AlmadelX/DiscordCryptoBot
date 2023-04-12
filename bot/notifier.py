import asyncio
from discord_markdown.discord_markdown import convert_to_html
from aiogram.utils.exceptions import ChatNotFound, BotBlocked
import re

from bot.bot import bot
from bot.models import Server, Subscription, User
from bot.resources.database import db_session


async def notify(users: list[int], message: str, parse_mode=''):
    calls = []
    for user in users:
        calls.append((
            asyncio.create_task(bot.send_message(
                user,
                message,
                parse_mode=parse_mode
            )),
            user
        ))

    to_delete = []
    for task, user in calls:
        try:
            await task
        except (ChatNotFound, BotBlocked):
            to_delete.append(user)

    if len(to_delete) > 0:
        db_session.query(Subscription).filter(Subscription.user_id.in_(to_delete)).delete()
        db_session.query(User).filter(User.id.in_(to_delete)).delete()
        db_session.commit()


def format_message(message: str) -> str:
    message = re.sub(r'<:\w*:\w*>', '', message)
    message = re.sub(r'<(\S*)>', r'\1', message)
    message = re.sub(r'@\w*', '', message)
    message = re.sub(r'\|\|(.*)\|\|', r'\1', message)

    message = convert_to_html(message)
    message = message.replace('<p>', '')
    message = message.replace('</p>', '\n')

    return message


async def notify_subscribers(server_id: int, announcement: str):
    server_name = db_session.query(Server).get(server_id).name
    subscriptions = db_session.query(
        Subscription
    ).filter_by(server_id=server_id).all()
    users = [subscription.user_id for subscription in subscriptions]
    message = '<b>Новый анонс от {}:</b>\n{}'.format(
        server_name,
        format_message(announcement)
    )

    await notify(users, message, 'HTML')


async def notify_all(message: str):
    users = db_session.query(User).all()
    ids = [user.id for user in users]

    await notify(ids, message)
