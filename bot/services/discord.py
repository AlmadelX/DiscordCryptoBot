import requests
import json

from bot.data.config import DISCORD_TOKEN
from bot.services.database import db_session
from bot.models import Server
from bot.utils.notifier import notify_subscribers

headers = {
    'authorization': DISCORD_TOKEN
}

async def poll_announcements():
    servers = db_session.query(Server).all()

    for server in servers:
        response = requests.get(
            f'https://discord.com/api/v9/channels/{server.channel}/messages?limit=1',
            headers=headers
        )
        message = json.loads(response.text)[0]
        if message['id'] == server.last_message:
            continue
        server.last_message = message['id']
        db_session.commit()

        text = message['content']
        announcement = f'New announcement on {server.name}:\n{text}'
        await notify_subscribers(server.id, announcement)


def get_last_message_id(channel: str) -> str:
    response = requests.get(
        f'https://discord.com/api/v9/channels/{channel}/messages?limit=1',
        headers=headers
    )
    if not response.ok:
        return 'error'
    
    message = json.loads(response.text)[0]
    return message['id']
