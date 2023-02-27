from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dicts.messages import start_survey_dict

"""
Клавиатуры для операторов
"""


class Operator_keyboard:
    def __init__(self, rows_in_line=1):
        self.rows_in_line = rows_in_line

    def confirm_new_user(self):
        new_user = InlineKeyboardMarkup(row_width=self.rows_in_line)
        button_1 = InlineKeyboardButton(text="Все ок", callback_data="new_user ok")
        button_2 = InlineKeyboardButton(text="Что то не так", callback_data="new_user not_ok")
        new_user.add(button_1, button_2)
        return new_user
