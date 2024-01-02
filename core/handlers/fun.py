from aiogram.filters.command import Command
from aiogram import types, Router


router = Router()


@router.message(Command("dice"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


@router.message(Command('reply_test'))
async def simple_reply(message: types.Message) -> None:
    await message.reply(text='Хорошая мысль, слушай!')


@router.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
