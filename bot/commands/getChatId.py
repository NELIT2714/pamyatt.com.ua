from aiogram import types
from aiogram.filters import Command

from bot import dp


@dp.message(Command("get_chat"))
async def get_chat(message: types.Message) -> None:
    await message.reply(f"{message.chat.id}")
