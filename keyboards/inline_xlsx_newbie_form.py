from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_kb(buttons_text: list, callback_data: list, row_width: int = 1) -> object:
    j = 0
    returned_keyboard = InlineKeyboardMarkup(row_width=row_width)
    for i in buttons_text:
        if i is not None:
            button = InlineKeyboardButton(text=i, callback_data=callback_data[j])
            returned_keyboard.add(button)
            j += 1
    return returned_keyboard


def create_kb_next(buttons_text: list, callback_data: list, row_width: int = 1) -> object:
    j = 0
    returned_keyboard = InlineKeyboardMarkup(row_width=row_width)
    for i in buttons_text:
        if i is not None:
            button = InlineKeyboardButton(text=i, callback_data=callback_data[j])
            returned_keyboard.add(button)
            j += 1
    button_next = InlineKeyboardButton(text="->", callback_data="xlsx_pagi next")
    returned_keyboard.add(button_next)
    return returned_keyboard


def create_kb_prev(buttons_text: list, callback_data: list, row_width: int = 1) -> object:
    j = 0
    returned_keyboard = InlineKeyboardMarkup(row_width=row_width)
    for i in buttons_text:
        if i is not None:
            button = InlineKeyboardButton(text=i, callback_data=callback_data[j])
            returned_keyboard.add(button)
            j += 1
    button_prev = InlineKeyboardButton(text="<-", callback_data="xlsx_pagi prev")
    returned_keyboard.add(button_prev)
    return returned_keyboard


def create_kb_mid(buttons_text: list, callback_data: list, row_width: int = 1) -> object:
    j = 0
    returned_keyboard = InlineKeyboardMarkup(row_width=row_width)
    for i in buttons_text:
        if i is not None:
            button = InlineKeyboardButton(text=i, callback_data=callback_data[j])
            returned_keyboard.add(button)
            j += 1
    button_prev = InlineKeyboardButton(text="<-", callback_data="xlsx_pagi prev")
    button_next = InlineKeyboardButton(text="->", callback_data="xlsx_pagi next")
    returned_keyboard.row(button_prev, button_next)
    return returned_keyboard


button_start = InlineKeyboardButton(text="Start it up !!!", callback_data="xlsx_start")
start_kb = InlineKeyboardMarkup(row_width=1).add(button_start)