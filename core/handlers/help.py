from aiogram import Bot
from aiogram.types import Message


async def show_help(message: Message, bot: Bot):
    await message.answer(f'Привет, {message.from_user.first_name}, это телеграм-бот "Прокачай свою жопу"\n'
                         f'Возможности бота:\n'
                         f'1. Записывать результаты тренировки по команде /record\n'
                         f'2. Просматривать результаты тренировок по команде /results\n'
                         f'3. Создавать упражнения по команде /create_exercise\n'
                         f'4. Просматривать список всех упражнений по команде /get_exercises')
