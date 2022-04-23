from aiogram import types
from data import config
from loader import dp
from utils.work_with_db import SQLite

db = SQLite()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id, str(message.from_user.username))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Кнопк1', 'Кнопка2', 'Кнопка3']

    if str(message.from_user.id) in config.admins:
        buttons.append('Кнопка4')
        buttons.append('Кнопка5')
    markup.add(*buttons)
    await message.answer(f"🤘 Салют, {message.chat.username}!\n",
                         reply_markup=markup)
