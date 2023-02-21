from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""
Клавиатура для поиска людей в компании
"""

search_way = InlineKeyboardMarkup(row_width=1)
button_1 = InlineKeyboardButton(text="Поиск по фамилии", callback_data="search_by_name")
button_2 = InlineKeyboardButton(text="Поиск по должности", callback_data="search_by_title")
search_way.add(button_1, button_2)

