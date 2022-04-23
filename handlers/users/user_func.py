from aiogram import types
from loader import dp


@dp.message_handler(text="Кнопка1")
async def vk(message: types.Message):
    await message.answer("test")
