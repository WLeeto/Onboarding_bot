from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура для работы с оператором


def ask_operator(question_id):
    button_1 = InlineKeyboardButton(text="Отправить вопрос оператору", callback_data=f"call_operator {question_id}")
    call_operator_kb = InlineKeyboardMarkup(row_width=1).add(button_1)
    return call_operator_kb


def operator_choice_kb_gen():
    button_1 = InlineKeyboardButton(text="Ввести ответ вручную", callback_data="choice manual")
    button_2 = InlineKeyboardButton(text="Выбрать ответ из списка", callback_data="choice from")
    operator_choice_kb = InlineKeyboardMarkup(row_width=1).add(button_1, button_2)
    return operator_choice_kb


def operator_start_answering():
    button_1 = InlineKeyboardButton(text="Ответить", callback_data="help_with_answer")
    operator_start_answering_kb = InlineKeyboardMarkup(row_width=1).add(button_1)
    return operator_start_answering_kb