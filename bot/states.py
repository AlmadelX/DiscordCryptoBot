from aiogram.dispatcher.filters.state import State, StatesGroup


class ChooseLanguage(StatesGroup):
    choose_language = State()


class Subscribe(StatesGroup):
    confirm = State()
