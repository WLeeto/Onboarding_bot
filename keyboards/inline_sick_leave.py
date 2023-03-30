from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""
Клавиатуры для команды /sick_leave
"""

button_1 = InlineKeyboardButton(text="Больничный", callback_data="sick info")
button_2 = InlineKeyboardButton(text="Как считается оплата больничного?", callback_data="sick payment")
sick_leave_kb = InlineKeyboardMarkup(row_width=1).add(button_1, button_2)