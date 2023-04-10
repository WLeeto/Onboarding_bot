from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline_get_documents import get_annual_leave_button, get_vacation_at_own_button

"""
Клавиатура для редактирования стартовой анкеты
"""

button_1 = InlineKeyboardButton(text="ФИО", callback_data="change name")
button_2 = InlineKeyboardButton(text="Дату рождения", callback_data="change birth")
button_3 = InlineKeyboardButton(text="Телефон", callback_data="change phone")
button_4 = InlineKeyboardButton(text="Почта", callback_data="change e-mail")
button_5 = InlineKeyboardButton(text="Хобби", callback_data="change hobbie")

change_newbie_questioning = InlineKeyboardMarkup(row_width=1).add(button_1, button_2, button_3, button_4, button_5)
