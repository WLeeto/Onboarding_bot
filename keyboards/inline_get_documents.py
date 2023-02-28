from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""
Клавиатуры для вывода кнопки для скачивания документов
"""

get_annual_leave = InlineKeyboardMarkup(row_width=1)
button_1 = InlineKeyboardButton(text="Скачать заявление на ежегодный отпуск",
                                callback_data="get annual_leave_application")
get_annual_leave.add(button_1)


