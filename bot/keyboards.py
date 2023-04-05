from aiogram.types import ReplyKeyboardMarkup

from bot.data.config import get_admins
from bot.data.texts import load_text


def start_menu(user_id: int) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(load_text('servers_btn', user_id),
                 load_text('subscriptions_btn', user_id))
    keyboard.row(load_text('subscribe_all_btn', user_id), load_text(
        'subscribe_btn', user_id), load_text('unsubscribe_btn', user_id))
    keyboard.row(load_text('language_btn', user_id),
                 load_text('support_btn', user_id))

    if user_id in get_admins():
        keyboard.row(load_text('admin_btn', user_id))

    return keyboard


def language_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row('English', 'Русский')

    return keyboard


def confirm_menu(user_id: int) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(load_text('yes_btn', user_id), load_text('no_btn', user_id))

    return keyboard


def back_menu(user_id: int) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(load_text('back_btn', user_id))

    return keyboard

def admin_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row('Add server')
    keyboard.row('Get my ID')
    keyboard.row('Back')

    return keyboard
