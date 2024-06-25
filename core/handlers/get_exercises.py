import logging

import aiogram.exceptions
from aiogram import Bot
from aiogram.types import Message
from sqlalchemy import select

from core.db.db_config import engine
from core.db.exercises_table import exercises


async def get_exercises(message: Message, bot: Bot):
    stmt = select(exercises).order_by(exercises.c.id)
    async with engine.connect() as connect:
        exercises_list_db = await connect.execute(statement=stmt)
    result = '--------------------------------------------------------------------------------------------\n'
    for i in exercises_list_db:
        result += (f'Название упражнения: {i[1]}\n'
                   f'Инвентарь: {i[2]}\n')
        result += '--------------------------------------------------------------------------------------------\n'
    if result == '--------------------------------------------------------------------------------------------\n':
        result = ''
    try:
        await message.answer(result)
    except aiogram.exceptions.TelegramBadRequest:
        await message.answer('Список упражнений отсутствует\n'
                             'Введите команду /create_exercise, чтобы добавить упражнение')
