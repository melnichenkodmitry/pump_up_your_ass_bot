from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from sqlalchemy import select

from core.db.db_config import engine_async, engine_sync
from core.db.exercises_table import exercises

reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Ряд 1. Кнопка 1.'
        ),
        KeyboardButton(
            text='Ряд 1. Кнопка 2.'
        ),
        KeyboardButton(
            text='Ряд 1. Кнопка 3.'
        )
    ],
    [
        KeyboardButton(
            text='Ряд 2. Кнопка 1.'
        ),
        KeyboardButton(
            text='Ряд 2. Кнопка 2.'
        ),
        KeyboardButton(
            text='Ряд 2. Кнопка 3.'
        ),
        KeyboardButton(
            text='Ряд 2. Кнопка 4.'
        )
    ],
    [
        KeyboardButton(
            text='Ряд 3. Кнопка 1.'
        ),
        KeyboardButton(
            text='Ряд 3. Кнопка 2.'
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выберите кнопку', selective=True)

loc_tel_poll_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Отправить геолокацию',
            request_location=True
        )
    ],
    [
        KeyboardButton(
            text='Отправить свой контакт',
            request_contact=True
        )
    ],
    [
        KeyboardButton(
            text='Создать викторину',
            request_poll=KeyboardButtonPollType()
        )
    ]
], resize_keyboard=True, one_time_keyboard=False,
    input_field_placeholder='Отправь локацию, номер телефона или викторину/опрос')


def get_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text='Кнопка 1')
    keyboard_builder.button(text='Кнопка 2')
    keyboard_builder.button(text='Кнопка 3')
    keyboard_builder.button(text='Отправить геолокацию', request_location=True)
    keyboard_builder.button(text='Отправить свой контакт', request_contact=True)
    keyboard_builder.button(text='Создать викторину', request_poll=KeyboardButtonPollType())
    keyboard_builder.adjust(3, 2, 1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True,
                                      input_field_placeholder='Отправь локацию, номер телефона или викторину/опрос')


def get_exercises():
    keyboard_builder = ReplyKeyboardBuilder()
    stmt = select(exercises.c.exercise_name)
    with engine_async.connect() as connect:
        exercises_list = connect.execute(statement=stmt)
    for i in exercises_list:
        keyboard_builder.button(text=i[0])
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True,
                                      input_field_placeholder='Выберите упражнение')
