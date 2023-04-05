from bot.data.loader import bot
from bot.data.texts import load_text
from bot.models import Server, Subscription
from bot.services.database import db_session


async def notify_subscribers(server_id: int, announcement: str):
    server_name = db_session.query(Server).get(server_id).name
    subscriptions = db_session.query(
        Subscription
    ).filter_by(server_id=server_id).all()

    for subscription in subscriptions:
        message = '{} {}:\n{}'.format(
            load_text('announcement', subscription.user_id),
            server_name,
            announcement
        )
        await bot.send_message(subscription.user_id, message)
