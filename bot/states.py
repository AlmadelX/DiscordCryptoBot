from aiogram.dispatcher.filters.state import State, StatesGroup


class Language(StatesGroup):
    choose = State()


class SubscribeAll(StatesGroup):
    confirm = State()


class Subscribe(StatesGroup):
    input = State()


class Unsubscribe(StatesGroup):
    input = State()


class Support(StatesGroup):
    input = State()
