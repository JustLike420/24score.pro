from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import admins


# Проверка на написания сообщения в ЛС бота
class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


# Проверка на админа
class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        if str(message.from_user.id) in admins:
            return True
        else:
            return False
