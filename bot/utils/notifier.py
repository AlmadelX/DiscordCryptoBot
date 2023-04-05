from bot.services.database import db_session
from bot.models import Subscription
from bot.data.loader import bot


async def notify_subscribers(server_id: int, announcement: str):
    subscriptions = db_session.query(Subscription).filter_by(server_id=server_id).all()
    for subscription in subscriptions:
        await bot.send_message(subscription.user_id, announcement)
