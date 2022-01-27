from aiogram.dispatcher.filters.state import State, StatesGroup


class ExStates(StatesGroup):
    single = State()
    pair_first = State()
    pair_second = State()
