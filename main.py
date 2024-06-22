import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio

from core.handlers.callback import select_macbook
from core.settings import settings
from core.handlers.basic import get_start, get_photo, get_hello, get_location, get_inline
from core.utils.commands import set_commands
from aiogram.filters import CommandStart, Command
from core.utils.callbackdata import MacInfo

default = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=settings.bots.bot_token, default=default)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - [%(levelname)s] - (%(filename)s).%(funcName)s(%(lineno)d)'
                           '- %(message)s')


async def start_bot(bot: Bot):
    await set_commands(bot)
    # await bot.send_message(settings.bots.admin_id, text='Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен!')


async def start():
    dp.startup.register(start_bot)
    # dp.shutdown.register(stop_bot)
    dp.message.register(get_start, CommandStart())
    dp.message.register(get_location, F.location)
    dp.message.register(get_inline, Command(commands='inline'))
    dp.message.register(get_photo, F.photo)
    dp.message.register(get_hello, F.text.regexp('^Привет$|^привет$|^Hello$|^hello$'))
    dp.callback_query.register(select_macbook, MacInfo.filter(F.model == 'pro'))
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        logging.info('Exit')
