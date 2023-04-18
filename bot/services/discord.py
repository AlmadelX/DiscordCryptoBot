import asyncio
from aiohttp import ClientSession

from bot.resources.config import config
from bot.resources.database import db_session
from bot.models import Channel
from bot.notifier import notify_subscribers
from bot.resources.logging import logger

headers = {
    'authorization': config.discord_token
}


class Message:
    def __init__(self, id: int, text: str):
        self.id = id
        self.text = text


class DiscordException(Exception):
    def __init__(self):
        super().__init__('Failed to get message')


async def get_last_message(channel: str, session=ClientSession()) -> Message:
    async with session.get(
            f'https://discord.com/api/v9/channels/{channel}/messages?limit=1',
            headers=headers
    ) as response:
        if not response.ok:
            raise DiscordException()

        try:
            result = (await response.json())[0]
            return Message(result['id'], result['content'])
        except Exception:
            raise DiscordException()


async def poll_announcements():
    channels = db_session.query(Channel).all()

    notify_tasks = []
    async with ClientSession() as session:
        for channel in channels:
            try:
                message = await get_last_message(channel.id, session)
            except DiscordException:
                logger.error('Failed to read message from Discord')
                continue

            if message.id != channel.last_message:
                channel.last_message = message.id
                notify_tasks.append(
                    asyncio.create_task(notify_subscribers(channel.server, message.text))
                )

    db_session.commit()
    await asyncio.gather(*notify_tasks)


async def check_token() -> bool:
    test_channel = '1093044976281202810'

    try:
        await get_last_message(test_channel)
        return True
    except DiscordException:
        return False
