from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from create_bot import db

"""
Клавиатура для команды /projects
"""


projects_keyboard = InlineKeyboardMarkup(row_width=1)
all_projects_list = db.all_projects()
for i in all_projects_list:
    name = i.project_name
    id = i.id
    button = InlineKeyboardButton(text=name, callback_data=f"project {id}")
    projects_keyboard.add(button)

