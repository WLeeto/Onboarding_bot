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


back_to_name = InlineKeyboardButton(text="Назад (Ввести ФИО заново)", callback_data="back name")
back_to_name_kb = InlineKeyboardMarkup(row_width=1).add(back_to_name)

back_to_bdate = InlineKeyboardButton(text="Назад (Ввести дату рождения заново)", callback_data="back bdate")
back_to_bdate_kb = InlineKeyboardMarkup(row_width=1).add(back_to_bdate)

back_to_phone = InlineKeyboardButton(text="Назад (Ввести телефон заново)", callback_data="back phone")
back_to_phone_kb = InlineKeyboardMarkup(row_width=1).add(back_to_phone)

back_to_email = InlineKeyboardButton(text="Назад (Ввести email заново)", callback_data="back email")
back_to_email_kb = InlineKeyboardMarkup(row_width=1).add(back_to_email)
