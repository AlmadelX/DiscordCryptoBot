import requests
import json

from bot.resources.config import config
from bot.resources.database import db_session
from bot.models import Channel
from bot.notifier import notify_subscribers
from bot.resources.logging import logger

headers = {
    'authorization': config.discord_token
}


async def poll_announcements():
    channels = db_session.query(Channel).all()

    for channel in channels:
        response = requests.get(
            f'https://discord.com/api/v9/channels/{channel.id}/messages?limit=1',
            headers=headers
        )
        try:
            message = json.loads(response.text)[0]
            if message['id'] == channel.last_message:
                continue
            channel.last_message = message['id']
            db_session.commit()

            announcement = message['content']
            await notify_subscribers(channel.server, announcement)
        except Exception:
            logger.error('Failed to read message from Discord')


def get_last_message_id(channel: str) -> str:
    response = requests.get(
        f'https://discord.com/api/v9/channels/{channel}/messages?limit=1',
        headers=headers
    )
    if not response.ok:
        return 'error'

    message = json.loads(response.text)[0]
    return message['id']


def check_token() -> bool:
    test_channel = '1093044976281202810'
    return get_last_message_id(test_channel) != 'error'
