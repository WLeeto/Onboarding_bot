from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура для функции собраний (meeting)

button_1 = InlineKeyboardButton(text="Все верно, отправляем", callback_data="meeting yes")
button_2 = InlineKeyboardButton(text="Нет, давай заново", callback_data="meeting no")

meeting_kb = InlineKeyboardMarkup(row_width=1).add(button_1, button_2)