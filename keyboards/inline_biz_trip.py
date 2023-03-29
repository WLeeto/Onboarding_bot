from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""
Клавиатуры для логики отправки командировочных e-mail
"""

button_1 = InlineKeyboardButton(text="Все верно, отправляй", callback_data="form True")
button_2 = InlineKeyboardButton(text="Нет, давай заполним заново", callback_data="form False")
biz_trip_form_send_kb = InlineKeyboardMarkup(row_width=2).add(button_1, button_2)