import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram import Dispatcher
from core.handlers import basic, fun
import mysql.connector
from core.commands.commands import set_commands
from aiogram.client.session.aiohttp import AiohttpSession


load_dotenv()
TOKEN = getenv("BOT_TOKEN")


async def get_db_connector():
    config = {
        'user': getenv('USERNAME'),
        'password': getenv('DATABASE_PASS'),
        'host': getenv('DATABASE_HOST_ADDRESS'),
        'database': getenv('DATABASE_NAME'),
        'raise_on_warnings': True
    }

    # Создать подключение
    return mysql.connector.connect(**config)


async def main() -> None:
    # Special proxy for working in pythonanywhere
    session = AiohttpSession(proxy='http://proxy.server:3128')
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML, session=session)

    await set_commands(bot)

    connector = await get_db_connector()
    basic.set_db_connector(connector)

    dp = Dispatcher()
    dp.include_routers(basic.router, fun.router)

    await dp.start_polling(bot)

    # Закрыть подключение
    connector.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
