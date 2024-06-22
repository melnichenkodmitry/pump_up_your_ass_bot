from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.callbackdata import MacInfo

select_macbook = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Macbook Air 13" M1 2020',
            callback_data='apple_air_13_m1_2020'
        )
    ],
    [
        InlineKeyboardButton(
            text='Macbook Pro 14" M1 2021',
            callback_data='apple_pro_14_m1_2021'
        )
    ],
    [
        InlineKeyboardButton(
            text='Macbook Pro 16" M2 2019',
            callback_data='apple_pro_16_m2_2019'
        )
    ],
    [
        InlineKeyboardButton(
            text='Link',
            url='https://youtube.com'
        )
    ],
    [
        InlineKeyboardButton(
            text='Profile',
            url='tg://user?id=484818692'
        )
    ],
])


def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Macbook Air 13" M1 2020',
                            callback_data=MacInfo(model='air', size=13, chip='m1', year=2020))
    keyboard_builder.button(text='Macbook Pro 14" M1 2021',
                            callback_data=MacInfo(model='pro', size=14, chip='m1', year=2021))
    keyboard_builder.button(text='Macbook Pro 16" M2 2019',
                            callback_data=MacInfo(model='pro', size=16, chip='m2', year=2019))
    keyboard_builder.button(text='Link', url='https://youtube.com')
    keyboard_builder.button(text='Profile', url='tg://user?id=484818692')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
