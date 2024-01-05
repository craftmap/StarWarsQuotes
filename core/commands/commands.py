from aiogram import Bot, html
from aiogram.types import BotCommand, BotCommandScopeDefault, InlineKeyboardButton


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='rand',
            description='Выдать случайную цитату',
        ),
        BotCommand(
            command='help',
            description='Помощь',
        ),
        BotCommand(
            command='rand_from_chat',
            description=f'Выдать случайную цитату из этого чата',
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
