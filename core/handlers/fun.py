from aiogram.filters.command import Command
from aiogram import types, Router


router = Router()


@router.message(Command("dice"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


@router.message(Command('reply_test'))
async def simple_reply(message: types.Message) -> None:
    await message.reply(text='Хорошая мысль, слушай!')


@router.message(Command(''))
async def echo_handler(message: types.Message) -> None:
    await message.answer(
        '<b>Ошибка:</b> неизвестная команда.\n'
        'Используйте /help для информации'
    )
