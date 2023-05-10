import asyncio
import os
from contextlib import suppress

from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
from create_bot import db

from aiogram import types

from fuzzywuzzy import fuzz

from dicts.messages import start_survey_dict

from datetime import datetime

from email_validate import validate


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("contacts", "Контакты всех отделов"),
        types.BotCommand("vacation", "Подготовка к отпуску "),
        types.BotCommand("benefits", "Информация о бонусах компании и о способах получения"),
        types.BotCommand("support", "Помогает найти ответственного по вопросу"),
        types.BotCommand("social_media", "Ссылки на наши соцсети"),
        types.BotCommand("initiative", "Сбор инициатив/идей и предложений"),
        types.BotCommand("finance", "Вопросы по перечислениям"),
        types.BotCommand("bt", "Подготовка к командировке"),
        types.BotCommand("find", "Поиск контактных данных по фио, должности"),
        types.BotCommand("referal", "Информация о реферальной программе"),
        types.BotCommand("office", "Информация про офис"),
        types.BotCommand("tf360", "О проекте ТИМФОРС360.Цифровое спасибо"),
        types.BotCommand("projects", "Краткая информация о проектах"),
        types.BotCommand("about", "Информация о ТИМ ФОРС"),
        types.BotCommand("sick_leave", "Информация о больничном"),
        types.BotCommand("meeting", "Создать встречу"),
        types.BotCommand("bday", "Дни рождения сотрудников"),
    ])


async def delete_message(message: types.Message, sleep_time: int = 0):
    """
    Удаляет сообщение по истечению таймера sleep_time
    """
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


def recognize_question(question: str, questions: dict):
    sensitivity = 57
    recognized = {'id': '1', 'percent': 0}
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


def search_message(id: int, first_name: str, surname: str, patronymic: str, job_title: str, tg_name: str) -> str:
    contacts = db.find_contacts_by_id(id)
    if first_name is None:
        first_name = ""
    if surname is None:
        surname = ""
    if patronymic is None:
        patronymic = ""
    contacts_text = f"  └ <b>Email:</b> <code>{contacts.get('e-mail')}</code>\n" \
                    f"  └ <b>Phone:</b> <code>{contacts.get('phone')}</code>\n" \
                    f"  └ <b>Telegram:</b> <code>{tg_name}</code>"
    text = f"<i><u>{surname} {first_name} {patronymic}</u></i>\n" \
           f"<b>Должность:</b> {job_title}\n" \
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
            date_delta = datetime.now() - date
            if date_delta.days >= 5475:
                result = date
            else:
                result = False
        except ValueError as ex:
            print(ex)
            result = False
    else:
        result = False
    return result


def validate_date(date: str) -> bool:
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


def validate_phone(phone: str) -> str or False:
    replaced_phone = phone.replace(" ", "").replace("+", "")
    if replaced_phone.isdigit():
        if replaced_phone.startswith("7") or replaced_phone.startswith("8"):
            if len(replaced_phone) == 11:
                result = replaced_phone
            else:
                result = False
        else:
            result = False
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


def add_start_log(**kwargs):
    text = kwargs.get("text")
    with open("start_log.txt", "a", encoding="utf-8") as log:
        log.write(text)


def is_latin(string: str):
    """
    Проверяет строку на наличие чего-то кроме кирилицы.
    """
    lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return lower.intersection(string.lower()) != set()


def list_split(listA, n):
    return_list = []
    for x in range(0, len(listA), n):
        every_chunk = listA[x: n + x]
        if len(every_chunk) < n:
            every_chunk = every_chunk + \
                            [None for y in range(n - len(every_chunk))]
        return_list.append(every_chunk)
    return return_list


def create_pagi_data(text: list, list: list) -> dict:
    pagi_data = {
        "text": {},
        "cbq": {}
    }
    j = 0
    for i in text:
        pagi_data["text"][j] = i
        j += 1
    j = 0
    for i in list:
        pagi_data["cbq"][j] = i
        j += 1
    return pagi_data
