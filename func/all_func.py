import asyncio
from contextlib import suppress
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
from create_bot import db

from aiogram import types

from fuzzywuzzy import fuzz

from dicts.messages import start_survey_dict

question_list = db.find_all_questions()  # Лист всех вопросов сохранятся глобально


async def delete_message(message: types.Message, sleep_time: int = 0):
    """
    Удаляет сообщение по истечению таймера sleep_time
    """
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


def recognize_question(question: str, questions: dict):
    recognized = {'id': '', 'percent': 0}
    for key, value in questions.items():
        percent = fuzz.WRatio(question, value)
        if percent > recognized['percent']:
            recognized['id'] = key
            recognized['percent'] = percent
    if recognized['percent'] <= 50:
        print(f"!!! Совпадение запроса '{question}': {recognized['percent']}")
        result = None
    else:
        print(f"Совпадение запроса '{question}': {recognized['percent']}")
        result = recognized['id']
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
