import re

import aiogram.exceptions
import pytz
from aiogram import Bot
from aiogram.types import Message
from sqlalchemy import select

from core.db.db_config import engine_async
from core.db.exercises_table import exercises
from core.db.records_table import records
from core.db.users_table import users
from core.utils.db import check_registration


async def get_records(message: Message, bot: Bot):
    reg_status = await check_registration(username=message.from_user.username)
    if not reg_status:
        return await message.answer('Вы не зарегистрированы\n'
                                    'Пройдите регистрацию, используя команду /start')
    stmt = select(exercises.c.exercise_name, exercises.c.inventory_name, records.c.repeats, records.c.weight,
                  records.c.approaches, records.c.created_at).join(users, users.c.id == records.c.user_id).join(exercises,
                  exercises.c.id == records.c.exercise_id).where(
                  users.c.username == message.from_user.username).order_by(records.c.id)
    async with engine_async.connect() as connect:
        results_list_db = await connect.execute(statement=stmt)
    result = '---------------------------------------------------------------------------------------\n'
    for i in results_list_db:
        updated_data = i[5].replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Tomsk'))
        updated_data = re.sub(r'.{13}$', '', str(updated_data))
        result += (f'Название упражнения: {i[0]}\n'
                   f'Инвентарь: {i[1]}\n'  # Добавить название инвентаря
                   f'Количество повторений: {i[2]}\n'
                   f'Вес инвентаря: {i[3]}\n'
                   f'Количество подходов: {i[4]}\n'
                   f'Дата создания записи: {updated_data}\n')
        result += '---------------------------------------------------------------------------------------\n'
    if result == '---------------------------------------------------------------------------------------\n':
        result = ''
    try:
        await message.answer(result)
    except aiogram.exceptions.TelegramBadRequest:
        await message.answer('Записи упражнений отсутствуют\n'
                             'Введите команду /create_record, чтобы добавить новую запись')
