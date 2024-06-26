import sqlalchemy
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import insert

from core.db.db_config import engine
from core.db.exercises_table import exercises
from core.utils.db import check_registration
from core.utils.exercise import Exercise


async def ex_exercise_name(message: Message, state: FSMContext):
    reg_status = await check_registration(username=message.from_user.username)
    if not reg_status:
        return await message.answer('Вы не зарегистрированы\n'
                                    'Пройдите регистрацию, используя команду /start')

    await message.answer('Введите наименование упражнения')
    await state.set_state(Exercise.exercise_name)


async def inventory_name(message: Message, state: FSMContext):
    await state.update_data(exercise_name=message.text)
    await message.answer('Введите наименование инвентаря')
    await state.set_state(Exercise.inventory_name)


async def create_exercise(message: Message, state: FSMContext):
    await state.update_data(inventory_name=message.text)
    data = await state.get_data()
    exercise = data.get('exercise_name')
    inventory = data.get('inventory_name')
    stmt = insert(exercises).values([{
        'exercise_name': exercise,
        'inventory_name': inventory
    }])
    try:
        async with engine.connect() as connect:
            await connect.execute(statement=stmt)
            await connect.commit()
    except sqlalchemy.exc.IntegrityError:
        await message.answer(f'Упражнение "{exercise}" уже добавлено!')
    else:
        await message.answer(f'Упражнение добавлено успешно!')
    await state.clear()
