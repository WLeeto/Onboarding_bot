from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура для выбора типа оформления для команды /finance

button_1 = InlineKeyboardButton(text="Штат", callback_data="finance staff")
button_2 = InlineKeyboardButton(text="ИП/СЗ/ГПХ", callback_data="finance not_staff")
finance_staff_choose_kb = InlineKeyboardMarkup(row_width=1).add(button_1, button_2)