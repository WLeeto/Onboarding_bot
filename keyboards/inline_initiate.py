from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""
Клавиатуры для старта состояний
"""

start_sending_vacation_email_button = InlineKeyboardButton(text="Подать заявление на отпуск",
                                                           callback_data="initiate vaсation")
yes_button = InlineKeyboardButton(text="Да", callback_data="answer Да")
no_button = InlineKeyboardButton(text="Нет", callback_data="answer Нет")

start_sending_vacation_email_keyboard = InlineKeyboardMarkup(row_width=1).add(start_sending_vacation_email_button)
yes_no_keyboard = InlineKeyboardMarkup(row_width=1).add(yes_button, no_button)