from aiogram.dispatcher.filters.state import State, StatesGroup


class ChooseLanguage(StatesGroup):
    choose_language = State()


class SubscribeAll(StatesGroup):
    confirm = State()


class Subscribe(StatesGroup):
    input = State()


class Unsubscribe(StatesGroup):
    input = State()
