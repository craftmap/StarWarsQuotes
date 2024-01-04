from aiogram import Bot, html
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы',
        ),
        BotCommand(
            command='dice',
            description='Бросить кубик',
        ),
        BotCommand(
            command='rand',
            description='Выдать случайную цитату',
        ),
        BotCommand(
            command='help',
            description='Помощь',
        ),
        BotCommand(
            command='add',
            description=f'/add {html.bold(html.quote("<автор>: <цитата>"))} — добавить цитату',
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
