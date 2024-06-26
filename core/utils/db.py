import logging

from sqlalchemy import select

from core.db.db_config import engine
from core.db.exercises_table import exercises
from core.db.users_table import users


async def check_registration(username) -> bool:
    stmt = select(users.c.username).where(users.c.username == username)
    async with engine.connect() as connect:
        result = await connect.execute(statement=stmt)
        await connect.commit()
    try:
        if list(result)[0][0] == username:
            return True
    except IndexError:
        return False


async def check_exercise(exercise) -> bool:
    stmt = select(exercises.c.exercise_name).where(exercises.c.exercise_name == exercise)
    async with engine.connect() as connect:
        result = await connect.execute(statement=stmt)
        await connect.commit()
    try:
        if list(result)[0][0] == exercise:
            return True
    except IndexError:
        return False
