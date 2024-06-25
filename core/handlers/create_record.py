import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import insert, select

from core.db.db_config import engine
from core.db.records_table import records
from core.db.users_table import users
from core.utils.record import Record
from core.db.exercises_table import exercises


async def rec_exercise_name(message: Message, state: FSMContext):
    await message.answer('Введите название упражнения')
    await state.set_state(Record.exercise_name)


async def repeats(message: Message, state: FSMContext):
    await state.update_data(exercise_name=message.text)
    await message.answer('Введите количество повторений')
    await state.set_state(Record.repeats)


async def weight(message: Message, state: FSMContext):
    await state.update_data(repeats=message.text)
    await message.answer('Введите вес инвентаря, кг')
    await state.set_state(Record.weight)


async def approaches(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer('Введите количество подходов')
    await state.set_state(Record.approaches)


async def create_record(message: Message, state: FSMContext):
    await state.update_data(approaches=message.text)
    data = await state.get_data()
    exercise_name = data.get('exercise_name')
    repeats = data.get('repeats')
    weight = data.get('weight')
    approaches = data.get('approaches')
    user_id = select(users.c.id).where(users.c.username == message.from_user.username)
    exercise_id = select(exercises.c.id).where(exercises.c.exercise_name == exercise_name)
    stmt = insert(records).values([{
        'user_id': user_id,
        'exercise_id': exercise_id,
        'repeats': int(repeats),
        'weight': float(weight),
        'approaches': int(approaches)
    }])
    async with engine.connect() as connect:
        await connect.execute(statement=stmt)
        await connect.commit()
    await message.answer('Запись успешно добавлена!')
    await state.clear()
