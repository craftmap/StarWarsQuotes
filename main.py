import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram import Dispatcher
from core.handlers import basic, fun

from aiogram.client.session.aiohttp import AiohttpSession


load_dotenv()
TOKEN = getenv("BOT_TOKEN")


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    # Special proxy for wokring in pythonanywhere
    session = AiohttpSession(proxy='http://proxy.server:3128')
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML, session=session)

    dp = Dispatcher()
    dp.include_routers(basic.router, fun.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
