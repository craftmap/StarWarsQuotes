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

# TODO: выискивать в истории чата залайканное сообщение и выдавать его за цитату


def get_random_quote_from_table(table_name):
    with db_connection() as connection:
        cursor = connection.cursor()
        if not table_exist(table_name):
            return 'Похоже, вы ещё не добавляли цитат в этом чате🤷'
        cursor.execute(f'SELECT * FROM {table_name} ORDER BY RAND() LIMIT 1;')
        doc = cursor.fetchone()
        cursor.close()
        if not doc:
            return 'Похоже, вы ещё не добавляли цитат в этом чате🤷'
        if doc['quote_translation'] == '':
            return f'<b>Цитата</b>:\n' \
                   f'{doc["quote"]}\n' \
                   f'© <i>{doc["author_ru"]}</i>'
        else:
            return f'<b>Quote</b>:\n' \
                   f'{doc["quote"]}\n' \
                   f'©<i>{doc["author_en"]}</i>\n\n' \
                   f'<b>Цитата</b>:\n' \
                   f'<tg-spoiler>{doc["quote_translation"]}\n' \
                   f'© <i>{doc["author_ru"]}</i></tg-spoiler>'


@router.message(Command("rand"))
async def command_random_quote(message: Message) -> None:
    text = get_random_quote_from_table('quotes_star_wars')
    await message.answer(text)
    await message.bot.send_message(
        getenv('ADMIN_ID'),
        f'{message.from_user.full_name} command rand\nGot: {text}'
    )


@router.message(Command("rand_from_chat"))
async def command_random_quote(message: Message) -> None:
    text = get_random_quote_from_table(message.chat.username.title() + '_table')
    await message.answer(text)
    await message.bot.send_message(
        getenv('ADMIN_ID'),
        f'{message.from_user.full_name} command rand_from_chat\nGot: {text}'
    )


@router.message(Command("add"))
async def add_quote(
        message: Message,
        command: CommandObject
):
    if command.args is None:
        await message.answer(
            '<b>Ошибка</b>: не переданы аргументы. Пример:\n'
            f'/add Вася: А всё-таки она круглая!'
        )
        return
    try:
        author, quote = command.args.split(": ", maxsplit=1, )
    except ValueError:
        await message.answer(
            '<b>Ошибка</b>: неправильный формат команды. Пример:\n'
            f'/add Вася: бла-бла!'
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
                'quote_translation': '',
                'author_en': '',
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
        f'/rand_from_chat - Выдать случайную цитату из этого чата\n'
        f'/add {html.bold(html.quote("<автор>: <цитата>"))} — добавить цитату'
    )
    await message.bot.send_message(getenv('ADMIN_ID'), f'{message.from_user.full_name} command help\n')


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f'Hello, {hbold(message.from_user.full_name)}!')
