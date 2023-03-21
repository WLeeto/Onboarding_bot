from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""
Клавиатура для выбора типа трудоустройства
"""

button_1 = InlineKeyboardButton(text="Штат", callback_data="type_of_emp state")
button_2 = InlineKeyboardButton(text="ИП", callback_data="type_of_emp ip")
button_3 = InlineKeyboardButton(text="ГПХ", callback_data="type_of_emp gph")
button_4 = InlineKeyboardButton(text="СЗ", callback_data="type_of_emp sz")
type_of_employement_kb = InlineKeyboardMarkup(row_width=1).add(button_1, button_2, button_3, button_4)