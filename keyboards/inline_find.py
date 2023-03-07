from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""
Клавиатура для поиска людей в компании
"""


search_way = InlineKeyboardMarkup(row_width=1)
button_1 = InlineKeyboardButton(text="Поиск по имени", callback_data="search by_name")
button_2 = InlineKeyboardButton(text="Поиск по фамилии", callback_data="search by_surname")
button_3 = InlineKeyboardButton(text="Поиск по отчеству", callback_data="search by_patronymic")
button_4 = InlineKeyboardButton(text="Поиск по email", callback_data="search by_email")
button_5 = InlineKeyboardButton(text="Поиск по telegram ninckname", callback_data="search telegram_ninckname")
button_6 = InlineKeyboardButton(text="Поиск по должности", callback_data="search by_title")
button_7 = InlineKeyboardButton(text="Поиск по отделу", callback_data="search by_department")
button_8 = InlineKeyboardButton(text="Поиск по тегу", callback_data="search by_tag")
search_way.add(button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8)


