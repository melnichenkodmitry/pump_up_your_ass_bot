import logging
import re
import sys

import sqlalchemy.exc
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import insert, select

from core.db.db_config import engine
from core.db.records_table import records
from core.db.users_table import users
from core.utils.db import check_registration, check_exercise
from core.utils.record import Record
from core.db.exercises_table import exercises


def is_number_in_range_repeats_and_approaches(value):
    pattern = re.compile(r'^(?:[1-9]\d{0,2}|1000)$')
    if re.match(pattern, value):
        return True
    else:
        return False
    # return bool(re.match(r'^[1-9]?[0-9]{0,2}$', s))


def is_number_in_range_weight(value):
    pattern = re.compile(r'^(?:\d{1,3}(?:\.\d)?|1000\.0)$')
    if re.match(pattern, value):
        return True
    else:
        return False
    # return bool(re.match(r'^(?:[1-9]\d{0,2}|100[0-9]|1000)(?:\.\d{1})?$', s))


async def rec_exercise_name(message: Message, state: FSMContext):
    reg_status = await check_registration(username=message.from_user.username)
    if not reg_status:
        return await message.answer('Вы не зарегистрированы\n'
                                    'Пройдите регистрацию, используя команду /start')
    await message.answer('Введите наименование упражнения')
    await state.set_state(Record.exercise_name)


async def repeats(message: Message, state: FSMContext):
    exercise_status = await check_exercise(exercise=message.text)
    if not exercise_status:
        await state.clear()
        return await message.answer(f'Упражнение "{message.text}" не найдено\n'
                                    f'Введите команду /create_exercise, чтобы создать упражнение и повторите попытку')
    await state.update_data(exercise_name=message.text)
    await message.answer('Введите количество повторений')
    await state.set_state(Record.repeats)


async def weight(message: Message, state: FSMContext):
    if not is_number_in_range_repeats_and_approaches(message.text):
        await state.clear()
        return await message.answer('Принимаются значения от 1 до 1000\n'
                                    'Повторите попытку по команде /create_record')
    await state.update_data(repeats=message.text)
    await message.answer('Введите вес инвентаря, кг')
    await state.set_state(Record.weight)


async def approaches(message: Message, state: FSMContext):
    if not is_number_in_range_weight(message.text):
        await state.clear()
        return await message.answer('Принимаются значения от 1.0 до 1000.0 c одним знаком после запятой\n'
                                    'Повторите попытку по команде /create_record')
    await state.update_data(weight=message.text)
    await message.answer('Введите количество подходов')
    await state.set_state(Record.approaches)


async def create_record(message: Message, state: FSMContext):
    if not is_number_in_range_repeats_and_approaches(message.text):
        await state.clear()
        return await message.answer('Принимаются значения от 1 до 1000\n'
                                    'Повторите попытку по команде /create_record')
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
    try:
        async with engine.connect() as connect:
            await connect.execute(statement=stmt)
            await connect.commit()
    except sqlalchemy.exc.IntegrityError:
        await message.answer('Имя пользователя или название упражнения не найдено')
    else:
        await message.answer('Запись успешно добавлена!')
    finally:
        await state.clear()
