from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp, bot
from utils.other_func import get_menu, parse_table, push_csv_to_gsheet, find_sheet_id_by_name

hockey_menu = get_menu('hockey')
football_menu = get_menu('football')
basketball_menu = get_menu('basketball')


@dp.message_handler(text="Хоккей")
async def hockey(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    for link in hockey_menu:
        link = types.InlineKeyboardButton(text=link, callback_data=f'tour_hockey_{link}')
        markup.add(link)
    await bot.send_message(message.chat.id, "Выбери страну", reply_markup=markup)


@dp.message_handler(text="Футбол")
async def football(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    for link in football_menu:
        link = types.InlineKeyboardButton(text=link, callback_data=f'tour_football_{link}')
        markup.add(link)
    await bot.send_message(message.chat.id, "Выбери страну", reply_markup=markup)


@dp.message_handler(text="Баскетбол")
async def basketball(message: types.Message):
    markup = types.InlineKeyboardMarkup()

    for link in basketball_menu:
        link = types.InlineKeyboardButton(text=link, callback_data=f'tour_basketball_{link}')
        markup.add(link)
    await bot.send_message(message.chat.id, "Выбери страну", reply_markup=markup)


@dp.callback_query_handler(Text(startswith="tour_"))
async def handle_query_foot_link(call: types.CallbackQuery):
    markup2 = types.InlineKeyboardMarkup()
    action = call.data.split('_')
    sport = action[1]
    country = action[2]
    if sport == 'hockey':
        for links in hockey_menu[country]:
            name_tour = links.split(' | ')[0]
            link = types.InlineKeyboardButton(text=f'{name_tour}', callback_data=f't3_hockey_{country}_{name_tour}')
            markup2.add(link)
    elif sport == 'football':
        for links in football_menu[country]:
            name_tour = links.split(' | ')[0]
            link = types.InlineKeyboardButton(text=f'{name_tour}', callback_data=f't3_football_{country}_{name_tour}')
            markup2.add(link)
    elif sport == 'basketball':
        for links in basketball_menu[country]:
            name_tour = links.split(' | ')[0]
            link = types.InlineKeyboardButton(text=f'{name_tour}', callback_data=f't3_basketball_{country}_{name_tour}')
            markup2.add(link)
    await call.message.edit_reply_markup(markup2)


@dp.callback_query_handler(Text(startswith="t3_"))
async def handle_query_foot(call: types.CallbackQuery):
    action = call.data.split('_')
    sport = action[1]
    t_name = action[2]
    t_leag = action[3]
    if sport == 'hockey':
        league_list = hockey_menu[t_name]
        sheet_name = 'Hockey'
    elif sport == 'football':
        league_list = football_menu[t_name]
        sheet_name = 'Football'
    elif sport == 'basketball':
        league_list = basketball_menu[t_name]
        sheet_name = 'Basketball'
    for leag in league_list:
        if t_leag in leag:
            league_link = leag.split(' | ')[1]
            break
    await parse_table(league_link, t_leag)
    await bot.send_message(call.from_user.id, 'Парсинг')
    push_csv_to_gsheet(
        worksheet_name=sheet_name,
        sheet_id=find_sheet_id_by_name(sheet_name),
        column=0
    )
    await bot.send_message(call.from_user.id, 'Спаршено')
