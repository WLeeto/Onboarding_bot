from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""
Клавиатура для команды /projects
"""

# todo переделать, формировать динамически по запросу из БД
projects_keyboard = InlineKeyboardMarkup(row_width=1)
projects_keyboard_b1 = InlineKeyboardButton(text="B2BCloud", callback_data="projects B2BCloud")
projects_keyboard_b2 = InlineKeyboardButton(text="Skils Cloud", callback_data="projects Skils_Cloud")
projects_keyboard_b3 = InlineKeyboardButton(text="1C ERP", callback_data="projects 1C_ERP")
projects_keyboard_b4 = InlineKeyboardButton(text="ТФ360", callback_data="projects TF360")
projects_keyboard_b5 = InlineKeyboardButton(text="Smart Back Office", callback_data="projects Smart_Back_Office")
projects_keyboard_b6 = InlineKeyboardButton(text="Хакер Хоум", callback_data="projects Hacker_Home")
projects_keyboard_b7 = InlineKeyboardButton(text="Светлое", callback_data="projects Light")
projects_keyboard.add(projects_keyboard_b1, projects_keyboard_b2, projects_keyboard_b3, projects_keyboard_b4,
                      projects_keyboard_b5, projects_keyboard_b6, projects_keyboard_b7)
