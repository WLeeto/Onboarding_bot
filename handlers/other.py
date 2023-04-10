import asyncio
import os
from datetime import date

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.utils.exceptions import CantInitiateConversation, WrongFileIdentifier

from create_bot import dp, bot, db
from dicts.messages import start_survey_dict, message_dict, operator_list, commands_dict
from func.all_func import delete_message, recognize_question, start_survey_answers, is_breakes, \
    is_reply_keyboard, search_message, validate_bday, validate_phone, validate_email, is_latin
from handlers.meeting_handlers import meeting
from handlers.newbie_questioning_handlers import newbie_questioning
from handlers.vacation_handlers import vacation
from handlers.projects_handlers import projects
from handlers.operator_handlers import operator
from handlers.finance_handlers import finance
from handlers.business_trip_handlers import business_trip
from handlers.sick_leave_handlers import sick_leave
from keyboards.inline_operator import ask_operator, confirm_new_user

from keyboards.inline_start_survey import Survey_inlines_keyboards
from keyboards.all_keyboards import all_keyboards

from transliterate import translit

from States.states import FSM_newbie_questioning


# @dp.message_handler(content_types='text', state=None)
async def recognizing(message: types.Message):
    question_list = db.find_all_questions()
    response_id = recognize_question(message.text, question_list)
    if response_id:
        answer = db.find_answer_by_question_id(response_id)
        check_keyboards = is_reply_keyboard(answer)
        if check_keyboards:
            keyboard = all_keyboards[check_keyboards[-1]]
            await message.reply(is_breakes(check_keyboards[0]), reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        else:
            await message.reply(is_breakes(answer), parse_mode=types.ParseMode.HTML)
    else:
        question = db.add_new_operator_question(question_text=message.text,
                                                sender_tg_id=message.from_id,
                                                message_id=message.message_id)
        question_id = question.id
        question_from_user = question.from_user_id
        question_message_id = question.message_id
        await message.reply("На такой запрос у меня нет ответа. Передать вопрос оператору ?",
                            reply_markup=ask_operator(question_id, question_from_user, question_message_id))


# @dp.callback_query_handler(lambda c: c.data.startswith("get"), state=None)
async def get_document(callback_query: types.CallbackQuery):
    """
    Тут парсятся все запросы документов
    """
    if callback_query.data.split(" ")[1] == "annual_leave_application":
        file_path = "documents/1_application for annual leave.doc"
    elif callback_query.data.split(" ")[1] == "business_trip_regulation":
        file_path = "documents/2 regulations on official business trips.pdf"
    elif callback_query.data.split(" ")[1] == "official_memo":
        file_path = "documents/3 official memo.docx"
    elif callback_query.data.split(" ")[1] == "application_for_funds":
        file_path = "documents/4 application for funds.doc"
    elif callback_query.data.split(" ")[1] == "teamforce_presentation":
        file_path = "documents/5 teamforce presentation.pdf"
    elif callback_query.data.split(" ")[1] == "vacation_at_own":
        file_path = "documents/6 vacation_at_own.doc"
    else:
        file_path = None

    if file_path:
        with open(file_path, "rb") as file:
            await bot.send_document(chat_id=callback_query.from_user.id, document=file)
            await callback_query.answer()


# @dp.callback_query_handler(lambda c: c.data.startswith("contacts"), state=None)
async def get_contacts(callback_query: types.CallbackQuery):
    contact_type = callback_query.data.split(" ")[1]
    if contact_type == "hr":
        await callback_query.message.edit_text(commands_dict["contacts_hr"], parse_mode=types.ParseMode.HTML)
    elif contact_type == "contracts":
        await callback_query.message.edit_text(commands_dict["contacts_contracts"], parse_mode=types.ParseMode.HTML)
    elif contact_type == "resourses":
        await callback_query.message.edit_text(commands_dict["contacts_resourses"], parse_mode=types.ParseMode.HTML)


# Состояния для поиска сотрудника --------------------------------------------------------------------------------------
# todo Декомпозировать логику поиска в отдельный пакет
# todo Вынести класс состояний поиска в States
class FSM_search(StatesGroup):
    enter_name = State()
    enter_surname = State()
    enter_patronymic = State()
    enter_email = State()
    enter_tg_nickname = State()
    enter_department = State()
    enter_title = State()
    enter_phone = State()


# @dp.callback_query_handler(lambda c: c.data.startswith("search"), state=None)
async def search(callback_query: types.CallbackQuery, state: FSMContext):
    global answer
    if callback_query.data.split(" ")[1] == "by_name":
        await FSM_search.enter_name.set()
        answer = await bot.edit_message_text("Кого ищем ? (введи имя):",
                                             callback_query.from_user.id, callback_query.message.message_id)
    elif callback_query.data.split(" ")[1] == "by_surname":
        await FSM_search.enter_surname.set()
        answer = await bot.edit_message_text("Кого ищем ? (введи фамилию):",
                                             callback_query.from_user.id, callback_query.message.message_id)
    elif callback_query.data.split(" ")[1] == "by_title":
        await FSM_search.enter_title.set()
        answer = await bot.edit_message_text("Кого ищем ? (введите должность)",
                                             callback_query.from_user.id, callback_query.message.message_id)
    elif callback_query.data.split(" ")[1] == "by_patronymic":
        await FSM_search.enter_patronymic.set()
        answer = await bot.edit_message_text("Кого ищем ? (введите отчество)",
                                             callback_query.from_user.id, callback_query.message.message_id)
    elif callback_query.data.split(" ")[1] == "by_email":
        await FSM_search.enter_email.set()
        answer = await bot.edit_message_text("Кого ищем ? (введите почту)",
                                             callback_query.from_user.id, callback_query.message.message_id)
    elif callback_query.data.split(" ")[1] == "telegram_ninckname":
        await FSM_search.enter_tg_nickname.set()
        answer = await bot.edit_message_text("Кого ищем ? (введите ник в телеграме)",
                                             callback_query.from_user.id, callback_query.message.message_id)
    elif callback_query.data.split(" ")[1] == "by_department":
        await FSM_search.enter_department.set()
        answer = await bot.edit_message_text("Какой отдел ищем ? (введите название отдела)",
                                             callback_query.from_user.id, callback_query.message.message_id)
    elif callback_query.data.split(" ")[1] == "by_tag":
        await callback_query.answer("В разработке")
    elif callback_query.data.split(" ")[1] == "by_phone":
        await FSM_search.enter_phone.set()
        answer = await callback_query.message.edit_text("Введите последние 4 цифры телефона (например 4542)")
        await callback_query.answer()
    async with state.proxy() as data:
        data["answer"] = answer.message_id


# @dp.message_handler(content_types="text", state=FSM_search.enter_phone)
async def search_by_phone_step2(message: types.Message, state: FSMContext):
    result = db.particial_search_by_phone(message.text)
    async with state.proxy() as data:
        last_answer = data["answer"]
    if result:
        text = search_message(id=result.id, first_name=result.first_name, surname=result.surname,
                              job_title=result.job_title)
    else:
        text = f"Я не смог никого найти T_T, скорее всего пользователя с таким номером в базе нет"
    await state.finish()
    await delete_message(message, 0)
    await bot.edit_message_text(text, chat_id=message.from_id, message_id=last_answer, parse_mode=types.ParseMode.HTML)


# @dp.message_handler(content_types='text', state=FSM_search.enter_name)
async def search_by_name_step2(message: types.Message, state: FSMContext):
    result = db.find_by_name(message.text)
    await message.delete()
    async with state.proxy() as data:
        last_answer = data["answer"]
    if result:
        text = ''
        for i in result:
            text += search_message(i["id"], i["first_name"], i["surname"], i["job_title"])
        await bot.edit_message_text(text=f"<u>Вот, кого удалось найти:</u>\n\n{text}\n", chat_id=message.from_id,
                                    message_id=last_answer, parse_mode="html")
    else:
        await bot.edit_message_text(f"Я не нашел никого с именем {message.text} T_T", chat_id=message.from_id,
                                    message_id=last_answer, parse_mode=types.ParseMode.HTML)
        partial_search_result = db.partial_search_by_name(message.text)
        if partial_search_result:
            text = ''
            for i in partial_search_result:
                text += search_message(i["id"], i["first_name"], i["surname"], i["job_title"])
            await message.answer(text=f"<u>Вот, кто частично подходит под твой запрос:</u>\n\n{text}\n",
                                 parse_mode=types.ParseMode.HTML)
    await state.finish()


# @dp.message_handler(content_types='text', state=FSM_search.enter_surname)
async def search_by_surname_step2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        last_answer = data["answer"]
    result = db.find_by_surname(message.text)
    await message.delete()
    if result:
        text = ''
        for i in result:
            text += search_message(i["id"], i["first_name"], i["surname"], i["job_title"])
        await bot.edit_message_text(text=f"<u>Вот, кого удалось найти:</u>\n\n{text}\n", chat_id=message.from_id,
                                    message_id=last_answer, parse_mode=types.ParseMode.HTML)
        await state.finish()
    else:
        await bot.edit_message_text(f"Я не нашел никого с фамилией {message.text} T_T", chat_id=message.from_id,
                                    message_id=last_answer, parse_mode=types.ParseMode.HTML)
        partial_search_result = db.partial_search_by_surname(message.text)
        if partial_search_result:
            text = ''
            for i in partial_search_result:
                text += search_message(i["id"], i["first_name"], i["surname"], i["job_title"])
            await message.answer(text=f"<u>Вот, кто частично подходит под твой запрос:</u>\n\n{text}\n",
                                 parse_mode=types.ParseMode.HTML)
        await state.finish()


# @dp.message_handler(content_types='text', state=FSM_search.enter_patronymic)
async def search_by_patronymic_step2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        last_answer = data["answer"]
    result = db.find_by_patronymic(message.text)
    await message.delete()
    if result:
        text = ''
        for i in result:
            text += search_message(i["id"], i["first_name"], i["surname"], i["job_title"])
        await bot.edit_message_text(text=f"<u>Вот, кого удалось найти:</u>\n\n{text}\n", chat_id=message.from_id,
                                    message_id=last_answer, parse_mode=types.ParseMode.HTML)
        await state.finish()
    else:
        await bot.edit_message_text(f"Я не нашел никого с отчеством {message.text} T_T", chat_id=message.from_id,
                                    message_id=last_answer, parse_mode=types.ParseMode.HTML)
        partial_search_result = db.partial_search_by_patronymic(message.text)
        if partial_search_result:
            text = ''
            for i in partial_search_result:
                text += search_message(i["id"], i["first_name"], i["surname"], i["job_title"])
            await message.answer(text=f"<u>Вот, кто частично подходит под твой запрос:</u>\n\n{text}\n",
                                 parse_mode=types.ParseMode.HTML)
        await state.finish()


# @dp.message_handler(content_types='text', state=FSM_search.enter_title)
async def search_by_title_step2(message: types.Message, state: FSMContext):
    result = db.find_by_title(message.text)
    await message.delete()
    async with state.proxy() as data:
        last_answer = data["answer"]
    if result:
        text = ''
        for i in result:
            text += search_message(i["id"], i["first_name"], i["surname"], i["job_title"])
        await bot.edit_message_text(text=f"<u>Вот, кого удалось найти:</u>\n\n{text}\n", chat_id=message.from_id,
                                    message_id=last_answer, parse_mode=types.ParseMode.HTML)
        await state.finish()
    else:
        await bot.edit_message_text(f"Я не нашел никого с должностью {message.text} T_T", chat_id=message.from_id,
                                    message_id=last_answer, parse_mode=types.ParseMode.HTML)
        partial_search_result = db.partial_search_by_title(message.text)
        if partial_search_result:
            text = ''
            for i in partial_search_result:
                text += search_message(i["id"], i["first_name"], i["surname"], i["job_title"])
            await message.answer(text=f"<u>Вот, кто частично подходит под твой запрос:</u>\n\n{text}\n",
                                 parse_mode=types.ParseMode.HTML)
        await state.finish()


# @dp.message_handler(content_types='text', state=FSM_search.enter_tg_nickname)
async def search_by_tg_nickname_step2(message: types.Message, state: FSMContext):
    result = db.find_by_telegram_ninckname(message.text)
    await message.delete()
    async with state.proxy() as data:
        last_answer = data["answer"]
    if result:
        text = ''
        for i in result:
            text += search_message(i["id"], i["first_name"], i["surname"], i["job_title"])
        await bot.edit_message_text(text=f"<u>Вот, кого удалось найти:</u>\n\n{text}\n",
                                    chat_id=message.from_id, message_id=last_answer, parse_mode=types.ParseMode.HTML)
        await state.finish()
    else:
        await bot.edit_message_text(f"Я не нашел никого с ником {message.text} T_T", chat_id=message.from_id,
                                    message_id=last_answer, parse_mode=types.ParseMode.HTML)
        partial_search_result = db.partial_search_by_telegram_ninckname(message.text)
        if partial_search_result:
            text = ''
            for i in partial_search_result:
                text += search_message(i["id"], i["first_name"], i["surname"], i["job_title"])
            await message.answer(text=f"<u>Вот, кто частично подходит под твой запрос:</u>\n\n{text}\n",
                                 parse_mode=types.ParseMode.HTML)
        await state.finish()


# @dp.message_handler(content_types='text', state=FSM_search.enter_email)
async def search_by_email_step2(message: types.Message, state: FSMContext):
    result = db.find_by_email(message.text)
    await message.delete()
    async with state.proxy() as data:
        last_answer = data["answer"]
    if result:
        text = ''
        for i in result:
            text += search_message(i["id"], i["first_name"], i["surname"], i["job_title"])
        await bot.edit_message_text(text=f"<u>Вот, кого удалось найти:</u>\n\n{text}\n",
                                    chat_id=message.from_id, message_id=last_answer, parse_mode=types.ParseMode.HTML)
        await state.finish()
    else:
        await bot.edit_message_text(f"Я не нашел никого с почтой {message.text} T_T", chat_id=message.from_id,
                                    message_id=last_answer, parse_mode=types.ParseMode.HTML)
        partial_search_result = db.partial_search_by_email(message.text)
        if partial_search_result:
            text = ''
            for i in partial_search_result:
                text += search_message(i["id"], i["first_name"], i["surname"], i["job_title"])
            await message.answer(text=f"<u>Вот, кто частично подходит под твой запрос:</u>\n\n{text}\n",
                                 parse_mode=types.ParseMode.HTML)
        await state.finish()


# @dp.message_handler(content_types='text', state=FSM_search.enter_department)
async def search_by_department_step2(message: types.Message, state: FSMContext):
    result = db.find_department_by_name(message.text)
    await message.delete()
    async with state.proxy() as data:
        last_answer = data["answer"]
    if result:
        text = ''
        for i in result:
            text += f"{i['name']}:\n" \
                    f"Сотрудники:\n" \
                    f"{', '.join(i['employers'])}"
        await bot.edit_message_text(text=f"<u>Вот, что удалось найти:</u>\n\n{text}\n",
                                    chat_id=message.from_id, message_id=last_answer, parse_mode=types.ParseMode.HTML)
        await state.finish()
    else:
        await bot.edit_message_text(f"Я не нашел отдела {message.text} T_T", chat_id=message.from_id,
                                    message_id=last_answer, parse_mode=types.ParseMode.HTML)
        partial_search_result = db.find_department_particial_by_name(message.text)
        if partial_search_result:
            text = ''
            for i in partial_search_result:
                employers = "\n".join(i['employers'])
                text += f"<b>{i['name']}:</b>\n" \
                        f"<b>Сотрудники:</b>\n" \
                        f"{employers}"
            await message.answer(text=f"<u>Вот, кто частично подходит под твой запрос:</u>\n\n{text}\n",
                                 parse_mode=types.ParseMode.HTML)
        await state.finish()


# @dp.message_handler(content_types='video')
async def got_video(message: types.Message):
    await message.answer(f"Получил видео. Его id {message.video.file_id}")


# Состояния для опросника при старте работы ----------------------------------------------------------------------------
# todo декомпозировать опросник в отдельный пакет
# todo вынести класс состояний опросника в States
class FSM_start_survey(StatesGroup):
    first_question = State()
    second_question = State()
    third_question = State()
    compare_answers = State()


# @dp.callback_query_handler(lambda c: c.data == "start_survey", state=None)
async def first_question(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data.split(" ")[1] == "yes":
        keyboard = Survey_inlines_keyboards()
        await callback_query.answer()
        await FSM_start_survey.second_question.set()
        await bot.edit_message_text(f'Первый вопрос:\n{start_survey_dict["first_question_text"]}',
                                    chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=keyboard.first_question())
    else:
        await callback_query.answer()
        await bot.edit_message_text(start_survey_dict["wana_start_no_message"],
                                    chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id, )
        await state.finish()
        await asyncio.sleep(3)
        await callback_query.message.answer(message_dict.get("help_message"))


# @dp.callback_query_handler(
#     lambda c: c.data.startswith("first"),
#     state=FSM_start_survey.second_question
# )
async def second_question(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard = Survey_inlines_keyboards()
    async with state.proxy() as answers:
        answers['first'] = callback_query.data.split(" ")[1]
    await bot.edit_message_text(f'Второй вопрос:\n{start_survey_dict["second_question_text"]}',
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=keyboard.second_question())
    await callback_query.answer()
    await FSM_start_survey.third_question.set()


# @dp.callback_query_handler(
#     lambda c: c.data.startswith("second"),
#     state=FSM_start_survey.third_question
# )
async def third_question(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard = Survey_inlines_keyboards()
    async with state.proxy() as answers:
        answers['second'] = callback_query.data.split(" ")[1]
    await bot.edit_message_text(f'Третий вопрос:\n{start_survey_dict["third_question_text"]}',
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=keyboard.third_question())
    await callback_query.answer()
    await FSM_start_survey.compare_answers.set()


# @dp.callback_query_handler(
#     lambda c: c.data.startswith("third"),
#     state=FSM_start_survey.compare_answers
# )
async def answers(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as answers:
        answers['third'] = callback_query.data.split(" ")[1]
        all_answers = start_survey_answers(answer_1=answers['first'],
                                           answer_2=answers['second'],
                                           answer_3=answers['third'])

    await bot.edit_message_text(f"<u>Сверим ответы. Внимание на экран:</u>\n\n"
                                f"{all_answers}",
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                parse_mode="html"
                                )
    await callback_query.answer()
    await state.finish()
    await asyncio.sleep(3)
    await callback_query.message.answer(message_dict["we_are_closer_now"])
    await asyncio.sleep(3)
    text = db.find_answer_by_answer_id(31).answer_text
    await callback_query.message.answer(is_breakes(text), parse_mode=types.ParseMode.HTML)


# @dp.callback_query_handler(lambda c: c.data == "hr_contacts")
async def hr_contacts(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer(commands_dict["contacts_hr"], parse_mode=types.ParseMode.HTML)


def register_handlers_other(dp: Dispatcher):
    newbie_questioning.register_handlers_newbie_questioning(dp)
    meeting.register_handlers_meeting(dp)
    sick_leave.register_handlers_sick_leave(dp)
    vacation.register_handlers_vacation(dp)
    projects.register_handlers_projects(dp)
    operator.register_handlers_operator(dp)
    finance.register_handlers_finance(dp)
    business_trip.register_handlers_business_trip(dp)

    dp.register_callback_query_handler(hr_contacts, lambda c: c.data == "hr_contacts")

    dp.register_message_handler(recognizing, content_types='text', state=None)

    dp.register_callback_query_handler(get_contacts, lambda c: c.data.startswith("contacts"), state=None)

    dp.register_callback_query_handler(get_document, lambda c: c.data.startswith("get"), state=None)

    dp.register_callback_query_handler(search, lambda c: c.data.startswith("search"), state=None)
    dp.register_message_handler(search_by_surname_step2, content_types='text', state=FSM_search.enter_surname)
    dp.register_message_handler(search_by_title_step2, content_types='text', state=FSM_search.enter_title)
    dp.register_message_handler(search_by_name_step2, content_types='text', state=FSM_search.enter_name)
    dp.register_message_handler(search_by_patronymic_step2, content_types='text', state=FSM_search.enter_patronymic)
    dp.register_message_handler(search_by_tg_nickname_step2, content_types='text', state=FSM_search.enter_tg_nickname)
    dp.register_message_handler(search_by_email_step2, content_types='text', state=FSM_search.enter_email)
    dp.register_message_handler(search_by_department_step2, content_types='text', state=FSM_search.enter_department)
    dp.register_message_handler(search_by_phone_step2, content_types="text", state=FSM_search.enter_phone)

    dp.register_message_handler(got_video, content_types='video')

    dp.register_callback_query_handler(first_question, lambda c: c.data.startswith("survey"), state=None)
    dp.register_callback_query_handler(second_question, lambda c: c.data.startswith("first"),
                                       state=FSM_start_survey.second_question)
    dp.register_callback_query_handler(third_question, lambda c: c.data.startswith("second"),
                                       state=FSM_start_survey.third_question)
    dp.register_callback_query_handler(answers, lambda c: c.data.startswith("third"),
                                       state=FSM_start_survey.compare_answers)


