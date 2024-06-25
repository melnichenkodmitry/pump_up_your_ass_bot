from aiogram import Bot
from aiogram.types import BotCommandScopeDefault, BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Зарегистрироваться'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        ),
        BotCommand(
            command='create_record',
            description='Записать результат выполнения упражнений'
        ),
        BotCommand(
            command='get_records',
            description='Просмотреть результаты упражнений'
        ),
        BotCommand(
            command='create_exercise',
            description='Создать упражнение'
        ),
        BotCommand(
            command='get_exercises',
            description='Список всех упражнений'
        ),
        # BotCommand(
        #     command='inline',
        #     description='Показать инлайн клавиатуру'
        # )
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
