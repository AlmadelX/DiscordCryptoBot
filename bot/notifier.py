from bot.bot import bot
from bot.models import Server, Subscription
from bot.resources.database import db_session


async def notify_subscribers(server_id: int, announcement: str):
    server_name = db_session.query(Server).get(server_id).name
    subscriptions = db_session.query(
        Subscription
    ).filter_by(server_id=server_id).all()

    for subscription in subscriptions:
        message = 'Новый анонс от {}:\n{}'.format(
            server_name,
            announcement
        )
        await bot.send_message(subscription.user_id, message)
