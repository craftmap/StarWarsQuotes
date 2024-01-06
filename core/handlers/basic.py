from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from settings import GLOBAL_TABLE_NAME
from aiogram import Router
from aiogram.filters.command import Command, CommandObject
from aiogram import html
from core.data.utils import insert_data_to_db, table_exist, CREATE_TABLE_QUERY
import logging

from os import getenv
from db_connection import db_connection

router = Router()


# Идея: выискивать в истории чата залайканное сообщение и выдавать его за цитату
# Идея: редактировать цитаты?
# Идея: цитата дня с подходящей картинкой


def get_quote_message_from_doc(doc: dict) -> str:
    if doc['quote_translation'] == '':
        return f'<b>Цитата</b>:\n' \
               f'{doc["quote"]}\n' \
               f'© <i>{doc["author_ru"]}</i>'
    else:
        return f'<b>Quote</b>:\n' \
               f'{doc["quote"]}\n' \
               f'© <i>{doc["author_en"]}</i>\n\n' \
               f'<b>Цитата</b>:\n' \
               f'<tg-spoiler>{doc["quote_translation"]}\n' \
               f'© <i>{doc["author_ru"]}</i></tg-spoiler>'


def search_quote_with_words(table_name: str, words: str) -> str:
    with db_connection() as connection:
        cursor = connection.cursor()
        query = f"SELECT * FROM {{table_name}} WHERE {{field}} LIKE '%{words}%';"
        cursor.execute(query.format(table_name=table_name, field='quote'))
        doc = cursor.fetchone()
        if not doc:
            cursor.execute(query.format(table_name=table_name, field='quote_translation'))
            doc = cursor.fetchone()
        if not doc:
            cursor.execute(query.format(table_name=GLOBAL_TABLE_NAME, field='quote'))
            doc = cursor.fetchone()
        if not doc:
            cursor.execute(query.format(table_name=GLOBAL_TABLE_NAME, field='quote_translation'))
            doc = cursor.fetchone()
        words_list = words.split()
        or_query = " OR {field} LIKE '%{word}%'"
        if not doc:
            cursor.execute(query.format(table_name=table_name, field='quote')[:-1] +
                           f"{' '.join([or_query.format(field='quote', word=words_list[i]) for i in range(len(words_list))])};")
            doc = cursor.fetchone()
        if not doc:
            cursor.execute(query.format(table_name=GLOBAL_TABLE_NAME, field='quote')[:-1] +
                           f"{' '.join([or_query.format(field='quote', word=words_list[i]) for i in range(len(words_list))])};")
            doc = cursor.fetchone()
        if not doc:
            return f'Я не нашел цитату со {"словами" if len(words.split())>1 else "словом"} {words}🤷'
        return get_quote_message_from_doc(doc)


def get_random_quote_from_table(table_name, author: str = None):
    with db_connection() as connection:
        cursor = connection.cursor()
        if not table_exist(table_name):
            return 'Похоже, вы ещё не добавляли цитат в этом чате🤷'
        if author:
            author_query = (f" WHERE author_ru='{author[0].swapcase() + author[1:]}' "
                            f"OR author_ru='{author[0] + author[1:]}' "
                            f"OR author_en='{author[0].swapcase() + author[1:]}' "
                            f"OR author_en='{author[0] + author[1:]}' "
                            f"OR author_ru=' {author[0].swapcase() + author[1:]}' "
                            f"OR author_ru=' {author[0] + author[1:]}' ")
        cursor.execute(
            f'SELECT * FROM {table_name}{author_query if author else " "}ORDER BY RAND() LIMIT 1;'
        )
        doc = cursor.fetchone()
        cursor.close()
        if not doc:
            return 'Похоже, вы ещё не добавляли цитат в этом чате🤷'
        return get_quote_message_from_doc(doc)


async def notify_the_creator(message, command):
    await message.bot.send_message(
        getenv('ADMIN_ID'),
        f'{message.from_user.full_name} command <b>{command}</b>\n'
    )


def get_chat_title(message: Message) -> str:
    return (message.chat.username.title() if message.chat.type == 'private' else message.chat.title).replace(' ', '_')


@router.message(Command("rand"))
async def command_random_quote(message: Message) -> None:
    text = get_random_quote_from_table('quotes_star_wars')
    await message.answer(text)
    await notify_the_creator(message, 'rand')


@router.message(Command("rand_from_chat"))
async def command_random_quote_from_chat(message: Message) -> None:
    text = get_random_quote_from_table(get_chat_title(message) + '_table')
    await message.answer(text)
    await notify_the_creator(message, 'rand_from_chat')


@router.message(Command('author'))
async def command_quote_by_author(message: Message, command: CommandObject) -> None:
    if command.args is None:
        await message.answer(
            '<b>❌Ошибка</b>: не переданы аргументы. Пример:\n'
            f'/author Вася'
        )
        return
    table_name = get_chat_title(message) + '_table'
    text = get_random_quote_from_table(table_name, author=command.args.strip())
    await message.answer(text)
    await notify_the_creator(message, 'author')


@router.message(Command('search'))
async def command_search_by_words(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer(
            '<b>❌Ошибка</b>: не переданы аргументы. Пример:\n'
            f'/search морж'
        )
        return
    table_name = get_chat_title(message) + '_table'
    text = search_quote_with_words(table_name, words=command.args)
    await message.answer(text)
    await notify_the_creator(message, 'search')


@router.message(Command("add"))
async def add_quote(
        message: Message,
        command: CommandObject
):
    if command.args is None:
        await message.answer(
            '<b>❌Ошибка</b>: не переданы аргументы. Пример:\n'
            f'/add Вася: А всё-таки она круглая!'
        )
        return
    try:
        author, quote = command.args.split(": ", maxsplit=1, )
    except ValueError:
        await message.answer(
            '<b>❌Ошибка</b>: неправильный формат команды. Пример:\n'
            f'/add Вася: бла-бла!'
        )
        return
    table_name = get_chat_title(message) + '_table'
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
    await message.answer(f'<b>Цитата:</b> {author}: {quote} - добавлена успешно ✅')
    await notify_the_creator(message, 'add')


@router.message(Command("help"))
async def command_help(message: Message) -> None:
    await message.answer(
        '<b>Команды бота:</b>\n'
        '/rand — случайная цитата\n'
        f'/rand_from_chat - Выдать случайную цитату из этого чата\n'
        f'/author {html.bold(html.quote("<автор>"))} - Выдать цитату конкретного автора\n'
        f'/add {html.bold(html.quote("<автор>: <цитата>"))} — добавить цитату (В ОДНОМ сообщении)'
    )
    await notify_the_creator(message, 'help')


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f'Hello, {hbold(message.from_user.full_name)}!')
    await command_help(message)
    await notify_the_creator(message, 'start')


@router.message()
async def unknown_command(message: Message) -> None:
    if message.chat.type == 'private':
        await message.reply('Мне неизвестна эта команда🤷\nВот что я умею:')
        await command_help(message)
        await notify_the_creator(message, 'unknown')
