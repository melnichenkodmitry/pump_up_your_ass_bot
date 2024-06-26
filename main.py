import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio
from core.handlers.start import registration
from core.handlers.help import show_help, default_handler
from core.handlers.create_exercise import ex_exercise_name, inventory_name, create_exercise
from core.handlers.create_record import rec_exercise_name, weight, repeats, approaches, create_record
from core.handlers.get_exercises import get_exercises
from core.handlers.get_records import get_records
from core.utils.commands import set_commands
from aiogram.filters import CommandStart, Command
from core.utils.exercise import Exercise
from core.utils.record import Record

default = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=os.getenv('TOKEN'), default=default)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - [%(levelname)s] - (%(filename)s).%(funcName)s(%(lineno)d)'
                           '- %(message)s')


async def start_bot(bot: Bot):
    await set_commands(bot)
    # await bot.send_message(os.getenv('ADMIN_ID'), text='Бот запущен!')


async def stop_bot(bot: Bot):
    # await bot.send_message(os.getenv('ADMIN_ID'), text='Бот остановлен!')
    pass


async def start():
    dp.startup.register(start_bot)
    # dp.shutdown.register(stop_bot)
    dp.message.register(registration, CommandStart())

    dp.message.register(show_help, Command(commands='help'))

    dp.message.register(rec_exercise_name, Command(commands='create_record'))
    dp.message.register(repeats, Record.exercise_name)
    dp.message.register(weight, Record.repeats)
    dp.message.register(approaches, Record.weight)
    dp.message.register(create_record, Record.approaches)

    dp.message.register(get_records, Command(commands='get_records'))

    dp.message.register(ex_exercise_name, Command(commands='create_exercise'))
    dp.message.register(inventory_name, Exercise.exercise_name)
    dp.message.register(create_exercise, Exercise.inventory_name)

    dp.message.register(get_exercises, Command(commands='get_exercises'))
    dp.message.register(default_handler)
    # dp.message.register(get_start, CommandStart())
    # dp.message.register(get_location, F.location)
    # dp.message.register(get_inline, Command(commands='inline'))
    # dp.message.register(get_photo, F.photo)
    # dp.message.register(get_hello, F.text.regexp('^Привет$|^привет$|^Hello$|^hello$'))
    # dp.callback_query.register(select_macbook, MacInfo.filter(F.model == 'pro'))
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
