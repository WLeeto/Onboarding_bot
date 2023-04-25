from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_kb(buttons_text: list, callback_data: list, row_width: int = 1) -> object:
    j = 0
    returned_keyboard = InlineKeyboardMarkup(row_width=row_width)
    for i in buttons_text:
        button = InlineKeyboardButton(text=i, callback_data=callback_data[j])
        returned_keyboard.add(button)
        j += 1
    return returned_keyboard


button_start = InlineKeyboardButton(text="Start it up !!!", callback_data="xlsx_start")
start_kb = InlineKeyboardMarkup(row_width=1).add(button_start)