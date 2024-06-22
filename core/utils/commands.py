from aiogram import Bot
from aiogram.types import BotCommandScopeDefault, BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        ),
        BotCommand(
            command='commands',
            description='Список команд'
        ),
        BotCommand(
            command='cancel',
            description='Сбросить'
        ),
        BotCommand(
            command='inline',
            description='Показать инлайн клавиатуру'
        )
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
