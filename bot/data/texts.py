from bot.models import User, Text
from bot.services.db_session import db_session

def load_text(name: str, user_id: int) -> str:
    lang = db_session.query(User).get(user_id).lang
    text = db_session.query(Text).get(name)

    if lang == 'eng':
        return text.eng
    elif lang == 'rus':
        return text.rus
    
def load_button(name: str) -> list[str]:
    button = db_session.query(Text).get(name)

    return [button.eng, button.rus]