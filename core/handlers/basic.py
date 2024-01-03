from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram import Router
from aiogram.filters.command import Command
from mysql.connector.cursor import MySQLCursor
from typing import Optional
from os import getenv

router = Router()
_db_connector = None


def set_db_connector(connector):
    global _db_connector
    _db_connector = connector


@router.message(Command("rand"))
async def command_random_quote(message: Message) -> None:
    cursor: Optional[MySQLCursor] = _db_connector.cursor()
    table_name = 'quotes_static'
    cursor.execute(f'SELECT * FROM {table_name} ORDER BY RAND() LIMIT 1;')
    _, quote, quote_translation = cursor.__next__()
    await message.answer(f'<b>quote</b>:{quote}\n<b>цитата</b>:<tg-spoiler>{quote_translation}</tg-spoiler>')
    await message.bot.send_message(getenv('ADMIN_ID'), f'{message.from_user.full_name} command rand\nGot: {quote}')


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f'Hello, {hbold(message.from_user.full_name)}!')
