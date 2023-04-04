from bot.models import Language, Text
from bot.services.db_session import db_session

def load_text(name: str, user_id: int) -> str:
    lang = db_session.query(Language).get(user_id).lang
    text = db_session.query(Text).get(name)

    if lang == 'eng':
        return text.eng
    elif lang == 'rus':
        return text.rus