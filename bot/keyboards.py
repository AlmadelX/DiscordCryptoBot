from aiogram.types import ReplyKeyboardMarkup

from bot.resources.config import config


def admin_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row('Добавить сервер', 'Удалить сервер')
    keyboard.row('Узнать мой ID')
    keyboard.row('Рассылка')
    keyboard.row('Назад')

    return keyboard


def append_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Завершить', 'Назад')
    return keyboard


def back_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Назад')
    return keyboard


def confirm_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Да', 'Нет')
    return keyboard


def start_menu(user_id: int) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row('📝 Доступные серверы', '📚 Мои подписки')
    keyboard.row('📣 Подписаться на всё', '✅ Подписаться', '❌ Отписаться')
    keyboard.row('👨‍💻 Поддержка')

    if user_id in config.bot_admins:
        keyboard.row('Админ-панель')

    return keyboard
