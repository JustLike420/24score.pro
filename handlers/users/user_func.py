from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp, bot
from utils.other_func import get_menu, parse_table, push_csv_to_gsheet, find_sheet_id_by_name, parse_today, get_date_time
from utils.work_with_db import SQLite
from keyboards import buy_item_open_category_ap, buy_item_next_page_category_ap, buy_item_previous_page_category_ap
# составление меню выбора спорта
hockey_menu = get_menu('hockey')
football_menu = get_menu('football')
basketball_menu = get_menu('basketball')

db = SQLite()


# inline кнопки со странами
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

# inline кнопки с турнирами
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

# парсинг турнира
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
    times = get_date_time(league_link)
    markup2 = types.InlineKeyboardMarkup()
    for time in times:
        link = types.InlineKeyboardButton(text=f'{time}', callback_data=f't4_{sport}_{t_name}_{t_leag}_{time}')
        markup2.add(link)
    await call.message.edit_text("Выберите год", reply_markup=markup2)

    # await parse_table(league_link, t_leag)
    # await bot.send_message(call.from_user.id, 'Парсинг')
    # push_csv_to_gsheet(
    #     worksheet_name=sheet_name,
    #     sheet_id=find_sheet_id_by_name(sheet_name),
    #     column=0
    # )
    # await bot.send_message(call.from_user.id, 'Спаршено')
@dp.callback_query_handler(Text(startswith="t4_"))
async def handle_query_foot1(call: types.CallbackQuery):
    action = call.data.split('_')
    sport = action[1]
    t_name = action[2]
    t_leag = action[3]
    time = action[4]
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
    league_link = league_link.split('/')
    time = time.split('/')
    if len(time) == 2:
        time = time[0] + '-' + '20' + time[1]
    elif len(time) == 1:
        time = time[0]
    league_link[6] = time
    league_link = '/'.join(league_link)
    print(league_link)
    await parse_table(league_link, t_name+ ' ' + t_leag)
    await bot.send_message(call.from_user.id, 'Парсинг')
    push_csv_to_gsheet(
        worksheet_name=sheet_name,
        sheet_id=find_sheet_id_by_name(sheet_name),
        column=0
    )
    await bot.send_message(call.from_user.id, 'Спаршено')
# матчи сегодня выбор вида спорта
@dp.message_handler(text="Матчи сегодня")
async def today(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    football = types.InlineKeyboardButton(text=f'Футбол', callback_data=f'today_football')
    hockey = types.InlineKeyboardButton(text=f'Хоккей', callback_data=f'today_hockey')
    basketball = types.InlineKeyboardButton(text=f'Баскетбол', callback_data=f'today_basketball')
    markup.add(football)
    markup.add(hockey)
    markup.add(basketball)
    await bot.send_message(message.chat.id, "Выбери вид спорта", reply_markup=markup)

# парсинг матчей сегодня и вывод
champ_list_dict = {

}
@dp.callback_query_handler(Text(startswith="today_"))
async def today_tourner(call: types.CallbackQuery):
    markup2 = types.InlineKeyboardMarkup()
    action = call.data.split('_')
    sport = action[1]
    champ_list = parse_today(sport)
    champ_list_dict['champ_list'] = champ_list
    get_kb = buy_item_open_category_ap(0, champ_list, sport)
    # for champ in champ_list:
    #     name_tour = champ.split(' | ')[0].strip().replace(' ', '_')
    #     tour_link = champ.split(' | ')[1].split('/')
    #     tour_link = tour_link[2] + "/" + tour_link[3]
    #     link = types.InlineKeyboardButton(text=f'{name_tour}', callback_data=f'tt_{sport}_{tour_link}')
    #     markup2.add(link)
    # show = types.InlineKeyboardButton(text=f'Показать список на парсинг', callback_data=f'show_queue')
    # markup2.add(show)
    await call.message.edit_text("Выберите турнир", reply_markup=get_kb)
    # await call.message.edit_reply_markup(get_kb)

# Следующая страница категорий при покупке
@dp.callback_query_handler(text_startswith="buy_nextp", state="*")
async def buy_item_next_page_category(call: types.CallbackQuery):
    remover = int(call.data.split(":")[1])
    sport = call.data.split('_')[2].split(':')[0]
    await call.message.edit_text("Выберите турнир",
                                 reply_markup=buy_item_next_page_category_ap(remover, champ_list_dict['champ_list'], sport))


# Предыдущая страница категорий при покупке
@dp.callback_query_handler(text_startswith="buy_prevp", state="*")
async def buy_item_prev_page_category(call: types.CallbackQuery):
    remover = int(call.data.split(":")[1])
    sport = call.data.split('_')[2].split(':')[0]
    await call.message.edit_text("Выберите турнир",
                                 reply_markup=buy_item_previous_page_category_ap(remover, champ_list_dict['champ_list'], sport))

# добавление в очередь на парсинг
@dp.callback_query_handler(Text(startswith="tt_"))
async def today_tourner(call: types.CallbackQuery):
    sport = call.data.split('_')[1]
    tour_link = call.data.replace(f'tt_{sport}_', '')
    if sport == 'hockey':
        menu = hockey_menu
    elif sport == 'football':
        menu = football_menu
    elif sport == 'basketball':
        menu = basketball_menu
    for county, tours in menu.items():
        for tour in tours:
            link = tour.split(' | ')[1].replace('https://old.24score.pro/', '').split("/")
            link = link[1] + '/' + link[2]
            if link == tour_link:
                db.update_queue(tour)
                await call.answer(f"{tour.split(' | ')[0]} добавлен в очередь")

# показать очередь на парсинг
@dp.callback_query_handler(text="show_queue")
async def show_queue(call: types.CallbackQuery):
    queue = db.get_queue()
    send_message = ""
    for tour in queue:
        name = tour[0].split(' | ')[0]
        if send_message == "":
            send_message += name
        else:
            send_message += "\n" + name
    if send_message == "":
        send_message = "Очередь пустая"
    markup = types.InlineKeyboardMarkup()
    clear = types.InlineKeyboardButton(text=f'Очистить список', callback_data=f'clear_queue')
    start = types.InlineKeyboardButton(text=f'Запустить парсинг', callback_data=f'start_queue')
    markup.add(clear, start)
    await call.message.edit_text(send_message)
    await call.message.edit_reply_markup(markup)
    # await call.message.edit_text(send_message)
    # await bot.send_message(call.message.chat.id, send_message, reply_markup=markup)

# очистить очередь на парсинг
@dp.callback_query_handler(text="clear_queue")
async def clear_queue(call: types.CallbackQuery):
    db.clear_queue()
    await call.message.edit_text('Очередь очищена')

# запустить очередь на парсинг
@dp.callback_query_handler(text="start_queue")
async def clear_queue(call: types.CallbackQuery):
    queue = db.get_queue()
    col = 0
    for tour in queue:
        name = tour[0].split(' | ')[0]
        link = tour[0].split(' | ')[1]
        sport = link.replace('https://old.24score.pro/', '').split('/')[0]
        await parse_table(link, name)
        if sport == 'hockey':
            sheet_name = 'Hockey'
        elif sport == 'football':
            sheet_name = 'Football'
        elif sport == 'basketball':
            sheet_name = 'Basketball'
        push_csv_to_gsheet(
            worksheet_name=sheet_name,
            sheet_id=find_sheet_id_by_name(sheet_name),
            column=col
        )
        col += 6
    await bot.send_message(call.from_user.id, 'Спаршено')
    # db.clear_queue()
    # await call.message.edit_text('Очередь очищена')

