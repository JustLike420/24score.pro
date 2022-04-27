from aiogram import types
from filters import IsAdmin
from loader import dp


@dp.message_handler(IsAdmin(), text="admin")
async def admin(message: types.Message):
    await message.answer("admin_test")
