import sqlalchemy
from aiogram import Bot
from aiogram.types import Message
from sqlalchemy import insert

from core.db.db_config import engine
from core.db.users_table import users


async def registration(message: Message, bot: Bot):
    stmt = insert(users).values([{
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name
    }])
    try:
        async with engine.connect() as connect:
            await connect.execute(statement=stmt)
            await connect.commit()
    except sqlalchemy.exc.IntegrityError:
        await message.answer(f'{message.from_user.first_name}, вы уже зарегистрированы')
    else:
        await message.answer(f'Привет {message.from_user.first_name}!\n'
                             f'Регистрация прошла успешно')
