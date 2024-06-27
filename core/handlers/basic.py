import logging

import aiogram.exceptions
import sqlalchemy.exc
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import insert, select, delete

from core.db.db_config import engine_async
from core.db.exercises_table import exercises
from core.db.records_table import records
from core.db.users_table import users
from core.keyboards.reply import reply_keyboard, loc_tel_poll_keyboard, get_reply_keyboard
from core.keyboards.inline import select_macbook, get_inline_keyboard
from core.utils.exercise import Exercise


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
