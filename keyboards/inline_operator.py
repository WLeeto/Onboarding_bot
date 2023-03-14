from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура для работы с оператором


def ask_operator(question_id):
    button_1 = InlineKeyboardButton(text="Отправить вопрос оператору", callback_data=f"call_operator {question_id}")
    call_operator = InlineKeyboardMarkup(row_width=1).add(button_1)
    return call_operator
