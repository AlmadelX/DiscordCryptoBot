from aiogram.types import ReplyKeyboardMarkup

from bot.data.config import get_admins


def start_menu(user_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row("Available servers", "My subscriptions")
    keyboard.row("Subscribe to all", "Subscribe", "Unsubscribe")
    keyboard.row("Language", "Support")

    if user_id in get_admins():
        keyboard.row("Admin")

    return keyboard


def language_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row("Rus", "Eng")

    return keyboard
