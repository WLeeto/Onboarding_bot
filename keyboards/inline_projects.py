from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from create_bot import db

"""
Клавиатура для команды /projects
"""


class Projects_keyboard:
    def __init__(self):
        self.projects_keyboard = InlineKeyboardMarkup(row_width=1)
        self.all_projects_list = db.all_projects()

    def create_kb(self):
        for i in self.all_projects_list:
            self.projects_keyboard.add(InlineKeyboardButton(text=i.project_name, callback_data=f"project {i.id}"))
        return self.projects_keyboard
