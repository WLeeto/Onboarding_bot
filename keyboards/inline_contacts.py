from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""
Клавиатура для команды /contacts
"""

contacts_keyboard = InlineKeyboardMarkup(row_width=1)
contacts_keyboard_b1 = InlineKeyboardButton(text="Отдел кадров", callback_data="contacts hr")
contacts_keyboard_b2 = InlineKeyboardButton(text="Договорной отдел", callback_data="contacts contracts")
contacts_keyboard_b3 = InlineKeyboardButton(text="Ресурсный отдел", callback_data="contacts resourses")
contacts_keyboard_b4 = InlineKeyboardButton(text="Поиск коллеги по номеру телефону", callback_data="search by_phone")
contacts_keyboard.add(contacts_keyboard_b1, contacts_keyboard_b2, contacts_keyboard_b3, contacts_keyboard_b4)

start_search_by_phone = InlineKeyboardMarkup(row_width=1)
start_search_by_phone.add(contacts_keyboard_b4)