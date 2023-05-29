from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import db

# Клавиатура для работы с оператором


def ask_operator(question_id, question_from_user, question_message_id):
    button_1 = InlineKeyboardButton(text="Отправить вопрос оператору",
                                    callback_data=f"call_operator "
                                                  f"{question_id} {question_from_user} {question_message_id}")
    call_operator_kb = InlineKeyboardMarkup(row_width=1).add(button_1)
    return call_operator_kb


def operator_start_answering(question_id, question_from_user):
    button_1 = InlineKeyboardButton(text="Ответить",
                                    callback_data=f"help_with_answer {question_id} {question_from_user}")
    operator_start_answering_kb = InlineKeyboardMarkup(row_width=1).add(button_1)
    return operator_start_answering_kb


def operator_choice_kb_gen():
    button_1 = InlineKeyboardButton(text="Ввести ответ вручную", callback_data="choice manual")
    button_2 = InlineKeyboardButton(text="Выбрать ответ из списка", callback_data="choice from")
    operator_choice_kb = InlineKeyboardMarkup(row_width=1).add(button_1, button_2)
    return operator_choice_kb


def auto_answers_kb_gen():
    answers_list = db.all_answers()
    answers_kb = InlineKeyboardMarkup(row_width=1)
    manual_button = InlineKeyboardButton(text="Ввести ответ вручную", callback_data="auto_answer manual")
    for i in answers_list:
        if i.answer_discription:
            button = InlineKeyboardButton(text=i.answer_discription, callback_data=f"auto_answer {i.id}")
            answers_kb.add(button)
    answers_kb.add(manual_button)
    return answers_kb


def operator_add_new_question_kb_gen():
    button_1 = InlineKeyboardButton(text="Да", callback_data="add_answer yes")
    button_2 = InlineKeyboardButton(text="Нет", callback_data="add_answer no")
    operator_add_new_question_kb = InlineKeyboardMarkup(row_width=1).add(button_1, button_2)
    return operator_add_new_question_kb


def confirm_new_user(tg_id):
    button_1 = InlineKeyboardButton(text="Все ок", callback_data=f"new_user ok {tg_id}")
    button_2 = InlineKeyboardButton(text="Что-то не так", callback_data="new_user not_ok")
    new_user = InlineKeyboardMarkup(row_width=1).add(button_1, button_2)
    return new_user


def mail_or_card(tg_id):
    button_1 = InlineKeyboardButton(text="Заполнить заявку на почту", callback_data=f"operator mail")
    button_2 = InlineKeyboardButton(text="Отправить карточку в чат ТИМФОРС", callback_data=f"operator card {tg_id}")
    mail_or_card = InlineKeyboardMarkup(row_width=1).add(button_1, button_2)
    return mail_or_card


def edit_or_send():
    button_1 = InlineKeyboardButton(text="Редактировать увлечения", callback_data=f"operator edit")
    button_2 = InlineKeyboardButton(text="Запланировать отправку", callback_data=f"operator send")
    edit_or_send = InlineKeyboardMarkup(row_width=1).add(button_1, button_2)
    return edit_or_send
