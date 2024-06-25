from aiogram.fsm.state import StatesGroup, State


class Exercise(StatesGroup):
    exercise_name = State()
    inventory_name = State()
