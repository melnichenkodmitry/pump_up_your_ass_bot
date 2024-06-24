import logging

import aiogram.exceptions
import sqlalchemy.exc
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import insert, select, delete

from core.db.db_config import engine
from core.db.exercises_table import exercises
from core.db.users_table import users
from core.keyboards.reply import reply_keyboard, loc_tel_poll_keyboard, get_reply_keyboard
from core.keyboards.inline import select_macbook, get_inline_keyboard
from core.utils.exercise import Exercise


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


async def show_help(message: Message, bot: Bot):
    await message.answer(f'Привет, {message.from_user.first_name}, это телеграм-бот "Прокачай свою жопу"\n'
                         f'Возможности бота:\n'
                         f'1. Записывать результаты тренировки по команде /record\n'
                         f'2. Просматривать результаты тренировок по команде /results\n'
                         f'3. Создавать упражнения по команде /create_exercise\n'
                         f'4. Просматривать список всех упражнений по команде /get_exercises')


async def exercise_name(message: Message, state: FSMContext):
    await message.answer(f'Напишите название упражнения')
    await state.set_state(Exercise.exercise)


async def create_exercise(message: Message, state: FSMContext):
    await state.update_data(exercise_name=message.text)
    data = await state.get_data()
    exercise = data.get('exercise_name')
    stmt = insert(exercises).values([{
        'exercise_name': exercise
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


async def get_exercises(message: Message, bot: Bot):
    stmt = select(exercises).order_by(exercises.c.id)
    async with engine.connect() as connect:
        exercises_list_db = await connect.execute(statement=stmt)
    exercises_list = []
    for i in exercises_list_db:
        exercises_list.append(i[1])
    logging.info(list(enumerate(exercises_list)))
    result = ''
    for i, j in list(enumerate(exercises_list, 1)):
        result += f'{i}. {j}\n'
    try:
        await message.answer(result)
    except aiogram.exceptions.TelegramBadRequest:
        await message.answer(f'Список упражнений отсутствует.'
                             f'Для того, чтобы добавить упражнение введите команду /create_exercise')


async def get_inline(message: Message, bot: Bot):
    await message.answer(f'Привет, {message.from_user.first_name}. Показываю инлайн кнопки!',
                         reply_markup=get_inline_keyboard())


async def get_start(message: Message, bot: Bot):
    await message.answer(f'<s>Привет {message.from_user.first_name}</s>',
                         reply_markup=get_reply_keyboard())


async def get_location(message: Message, bot: Bot):
    await message.answer(f'Ты отправил локацию!\r\a'
                         f'{message.location.latitude}\r\n{message.location.longitude}')


async def get_photo(message: Message, bot: Bot):
    await message.answer('Ты отправил картинку, сохраню себе.')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, 'photo.jpg')


async def get_hello(message: Message, bot: Bot):
    await message.answer('И тебе привет!')
