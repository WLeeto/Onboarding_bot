from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_kb(buttons_text: list, callback_data: list, row_width: int = 1, buttons: int = 2,
              step: int = 0) -> object:
    j = 0
    returned_keyboard = InlineKeyboardMarkup(row_width=row_width)
    button_back = InlineKeyboardButton(text="<", callback_data="pagi back")
    button_forward = InlineKeyboardButton(text=">", callback_data="pagi forward")

    if len(buttons_text) > buttons:
        for i in buttons_text[step:buttons + step]:
            button = InlineKeyboardButton(text=i, callback_data=callback_data[j])
            returned_keyboard.add(button)
            j += 1
        if step == 0:
            returned_keyboard.add(button_forward)
        elif step >= len(buttons_text):
            returned_keyboard.add(button_back)
        else:
            returned_keyboard.add(button_back)
            returned_keyboard.add(button_forward)


    return returned_keyboard