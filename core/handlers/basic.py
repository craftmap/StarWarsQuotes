from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram import Router
from aiogram.filters.command import Command, CommandObject
from aiogram import html
from core.data.utils import insert_data_to_db, table_exist, CREATE_TABLE_QUERY

from os import getenv
from db_connection import db_connection

router = Router()


@router.message(Command("rand"))
async def command_random_quote(message: Message) -> None:
    with db_connection() as connection:
        cursor = connection.cursor()
        table_name = 'quotes_star_wars'
        cursor.execute(f'SELECT * FROM {table_name} ORDER BY RAND() LIMIT 1;')
        doc = cursor.fetchone()

        if doc['quote_translation'] != '':
            await message.answer(
                f'<b>Quote</b>:\n'
                f'{doc["quote"]}\n'
                f'©<i>{doc["author_en"]}</i>\n\n'
                f'<b>Цитата</b>:\n'
                f'<tg-spoiler>{doc["quote_translation"]}\n'
                f'©<i>{doc["author_ru"]}</i></tg-spoiler>')
        else:
            await message.answer(
                f'<b>Цитата</b>:\n'
                f'{doc["quote_translation"]}\n'
                f'©<i>{doc["author_ru"]}</i>')

        await message.bot.send_message(
            getenv('ADMIN_ID'),
            f'{message.from_user.full_name} command rand\nGot: {doc["quote"]}'
        )

        cursor.close()


@router.message(Command("add"))
async def add_quote(
        message: Message,
        command: CommandObject
):
    if command.args is None:
        await message.answer(
            '<b>Ошибка</b>: не переданы аргументы'
        )
        return
    try:
        author, quote = command.args.split(": ", maxsplit=1, )
    except ValueError:
        await message.answer(
            '<b>Ошибка</b>: неправильный формат команды. Пример:\n'
            f'/add_quote {html.bold(html.quote("Вася Пупкин: А всё-таки она круглая!"))}'
        )
        return

    chat_title = message.chat.username.title()
    table_name = chat_title + '_table'
    if not table_exist(table_name):
        with db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(CREATE_TABLE_QUERY.format(table_name=table_name))
            connection.commit()
            cursor.close()

    insert_data_to_db(
        data=[
            {
                'quote': quote,
                'quote_translation': '-1',
                'author_en': '-1',
                'author_ru': author,
            }
        ],
        table_name=table_name,
    )


@router.message(Command("help"))
async def command_random_quote(message: Message) -> None:
    await message.answer(
        '<b>Команды бота:</b>\n'
        '/rand — случайная цитата\n'
        f'/add_quote {html.bold(html.quote("<автор>: <цитата>"))} — добавить цитату'
    )
    await message.bot.send_message(getenv('ADMIN_ID'), f'{message.from_user.full_name} command help\n')


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f'Hello, {hbold(message.from_user.full_name)}!')
