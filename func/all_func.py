import asyncio
import os
from contextlib import suppress
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
from create_bot import db

from aiogram import types

from fuzzywuzzy import fuzz

from dicts.messages import start_survey_dict

import time
from datetime import datetime

from email_validate import validate


async def delete_message(message: types.Message, sleep_time: int = 0):
    """
    Удаляет сообщение по истечению таймера sleep_time
    """
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


def recognize_question(question: str, questions: dict):
    sensitivity = 55
    recognized = {'id': '', 'percent': 0}
    for key, value in questions.items():
        percent = fuzz.ratio(question.lower(), value.lower())
        if percent > recognized['percent']:
            recognized['id'] = key
            recognized['percent'] = percent
    if recognized['percent'] <= sensitivity:
        result_text = f"Совпадение слишком маленькое, вопрос не найден\n" \
                      f"Ближайшее совпадение '{question}' и '{db.find_question_by_question_id(recognized['id'])}':" \
                      f"{recognized['percent']}\n"
        result = None
    else:
        result_text = f"Совпадение запроса '{question}' и '{db.find_question_by_question_id(recognized['id'])}':" \
                      f"{recognized['percent']}\n"
        result = recognized['id']
    print(result_text)
    add_recognize_log(text=result_text)
    return result


def start_survey_answers(answer_1, answer_2, answer_3) -> str:
    return_text = ""
    if answer_1 == start_survey_dict["correct_first_answer"]:
        return_text += f"<b>Первый вопрос:</b>\n{start_survey_dict['first_question_text']}\n✅{answer_1}\n\n"
    else:
        return_text += f"<b>Первый вопрос:</b>\n{start_survey_dict['first_question_text']}\n❌{answer_1}\n" \
                       f"Верный ответ:\n✅{start_survey_dict['correct_first_answer']}\n\n"
    if answer_2 == start_survey_dict["correct_second_answer"]:
        return_text += f"<b>Второй вопрос:</b>\n{start_survey_dict['second_question_text']}\n✅{answer_2}\n\n"
    else:
        return_text += f"<b>Второй вопрос:</b>\n{start_survey_dict['second_question_text']}\n❌{answer_2}\n" \
                       f"Верный ответ:\n✅{start_survey_dict['correct_second_answer']}\n\n"
    if answer_3 == start_survey_dict["correct_third_answer"]:
        return_text += f"<b>Третий вопрос:</b>\n{start_survey_dict['third_question_text']}\n✅{answer_3}\n\n"
    else:
        return_text += f"<b>Третий вопрос:</b>\n{start_survey_dict['third_question_text']}\n❌{answer_3}\n" \
                       f"Верный ответ:\n✅{start_survey_dict['correct_third_answer']}\n\n"
    return return_text


def is_breakes(message):
    """
    Проверка есть ли в сообщении переносы \n
    """
    splitted = message.split(r"\n")
    result = ""
    for i in splitted:
        result += f"\n{i}"
    return result


def is_reply_keyboard(message: str):
    """
    Проверка есть ли в сообщении прикрепленная клавиатура
    """
    splited = message.split("#keyboard ")
    result = [i for i in splited]
    if len(result) > 1:
        return result
    else:
        return None


def search_message(id: int, first_name: str, surname: str, job_title: str) -> str:
    contacts = db.find_contacts_by_id(id)
    contacts_text = f"  <b>E-mail:</b> {contacts.get('e-mail')}\n" \
                    f"  <b>Phone:</b> {contacts.get('phone')}"
    text = f"<b>Имя:</b> {first_name}\n" \
           f"<b>Фамилия</b>: {surname}\n" \
           f"<b>Должность</b>: {job_title}\n" \
           f"<b>Отдел:</b> {db.find_department_by_user_id(id)}\n" \
           f"<b>Контакты:</b> \n{contacts_text}\n\n"

    return text


async def delete_temp_file(filepath):
    os.remove(filepath)
    print(f"Фаил {filepath} удален")


def validate_bday(date: str) -> bool:
    repl1 = date.replace("/", ".").replace("г", "").replace("Г", "").replace("г.", "")
    if len(repl1.split(".")) == 3:
        try:
            date = datetime.strptime(repl1, "%d.%m.%Y")
            result = date
        except ValueError as ex:
            print(ex)
            result = False
    else:
        result = False
    return result


def validate_phone(phone: str) -> bool:
    replace = phone.replace(" ", "").replace("+", "")
    if len(replace) == 11:
        result = replace
    else:
        result = False
    return result


def validate_email(email: str) -> bool:
    result = validate(email,
                      check_format=True,
                      check_blacklist=True,
                      check_dns=False,
                      dns_timeout=10,
                      check_smtp=False,  # Проверка действительно ли существует почта, инициировав SMTP-диалог
                      smtp_debug=False)
    return result


def add_recognize_log(**kwargs):
    text = kwargs.get("text")
    with open("recognize_log.txt", "a", encoding="utf-8") as log:
        log.write(text)
