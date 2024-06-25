import aiogram.exceptions
from aiogram import Bot
from aiogram.types import Message
from sqlalchemy import select

from core.db.db_config import engine
from core.db.exercises_table import exercises
from core.db.records_table import records
from core.db.users_table import users


async def get_records(message: Message, bot: Bot):
    stmt = select(exercises.c.exercise_name, exercises.c.inventory_name, records.c.repeats, records.c.weight,
                  records.c.approaches).join(users, users.c.id == records.c.user_id).join(exercises,
                  exercises.c.id == records.c.exercise_id).where(
                  users.c.username == message.from_user.username).order_by(records.c.id)
    async with engine.connect() as connect:
        results_list_db = await connect.execute(statement=stmt)
    result = '--------------------------------------------------------------------------------------------\n'
    for i in results_list_db:
        result += (f'Название упражнения: {i[0]}\n'
                   f'Инвентарь: {i[1]}\n'  # Добавить название инвентаря
                   f'Количество повторений: {i[2]}\n'
                   f'Вес инвентаря: {i[3]}\n'
                   f'Количество подходов: {i[4]}\n')
        result += '--------------------------------------------------------------------------------------------\n'
    if result == '--------------------------------------------------------------------------------------------\n':
        result = ''
    try:
        await message.answer(result)
    except aiogram.exceptions.TelegramBadRequest:
        await message.answer('Записи упражнений отсутствуют\n'
                             'Введите команду /record, чтобы добавить новую запись')
