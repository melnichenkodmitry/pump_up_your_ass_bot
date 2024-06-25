from aiogram.fsm.state import StatesGroup, State


class Record(StatesGroup):
    exercise_name = State()
    repeats = State()
    weight = State()
    approaches = State()
