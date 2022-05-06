from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

count_page = 10
def buy_item_open_category_ap(remover, get_categories, sport):
    x = 0
    keyboard = InlineKeyboardMarkup()
    # get_categories = get_all_categoriesx()
    for a in range(remover, len(get_categories)):
        if x < count_page:
            # link = get_categories[a].split(' | ')[1]
            tour_link = get_categories[a].split(' | ')[1].split('/')
            tour_link = tour_link[2] + "/" + tour_link[3]
            keyboard.add(InlineKeyboardButton(f"{get_categories[a].split(' | ')[0]}",
                                              callback_data=f"tt_{sport}_{tour_link}"))
        x += 1
    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > count_page and remover < 10:
        nomer_kb = InlineKeyboardButton("🔸 1 🔸", callback_data="...")
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"buy_nextp_{sport}:{remover + count_page}")
        keyboard.add(nomer_kb, next_kb)
    elif remover + count_page >= len(get_categories):
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"buy_prevp_{sport}:{remover - count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        keyboard.add(prev_kb, nomer_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"buy_nextp_{sport}:{remover + count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"buy_prevp_{sport}:{remover - count_page}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.add(InlineKeyboardButton(text=f'Показать список на парсинг', callback_data=f'show_queue'))
    return keyboard


# Следующая страница категорий при покупке товара
def buy_item_next_page_category_ap(remover, get_categories, sport):
    x = 0
    keyboard = InlineKeyboardMarkup()
    # get_categories = get_all_categoriesx()
    for a in range(remover, len(get_categories)):
        if x < count_page:
            tour_link = get_categories[a].split(' | ')[1].split('/')
            tour_link = tour_link[2] + "/" + tour_link[3]
            keyboard.add(InlineKeyboardButton(f"{get_categories[a].split(' | ')[0]}",
                                              callback_data=f"tt_{sport}_{tour_link}"))
        x += 1
    if remover + count_page >= len(get_categories):
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"buy_prevp_{sport}:{remover - count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        keyboard.add(prev_kb, nomer_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"buy_nextp_{sport}:{remover + count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"buy_prevp_{sport}:{remover - count_page}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.add(InlineKeyboardButton(text=f'Показать список на парсинг', callback_data=f'show_queue'))
    return keyboard


# Предыдующая страница категорий при покупке товара
def buy_item_previous_page_category_ap(remover, get_categories, sport):
    x = 0
    keyboard = InlineKeyboardMarkup()
    # get_categories = get_all_categoriesx()
    for a in range(remover, len(get_categories)):
        if x < count_page:
            tour_link = get_categories[a].split(' | ')[1].split('/')
            tour_link = tour_link[2] + "/" + tour_link[3]
            keyboard.add(InlineKeyboardButton(f"{get_categories[a].split(' | ')[0]}",
                                              callback_data=f"tt_{sport}_{tour_link}"))
        x += 1
    if remover <= 0:
        nomer_kb = InlineKeyboardButton("🔸 1 🔸", callback_data="...")
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"buy_nextp_{sport}:{remover + count_page}")
        keyboard.add(nomer_kb, next_kb)
    else:
        next_kb = InlineKeyboardButton("➡ Далее ➡",
                                       callback_data=f"buy_nextp_{sport}:{remover + count_page}")
        nomer_kb = InlineKeyboardButton(f"🔸 {str(remover + count_page)[:-1]} 🔸", callback_data="...")
        prev_kb = InlineKeyboardButton("⬅ Назад ⬅",
                                       callback_data=f"buy_prevp_{sport}:{remover - count_page}")
        keyboard.add(prev_kb, nomer_kb, next_kb)
    keyboard.add(InlineKeyboardButton(text=f'Показать список на парсинг', callback_data=f'show_queue'))
    return keyboard
