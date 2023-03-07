import asyncio
import os

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot, db
from dicts.messages import sleep_timer, start_survey_dict, message_dict, operator_list
from func.all_func import question_list, delete_message, recognize_question, start_survey_answers, is_breakes, \
    is_reply_keyboard, search_message, delete_temp_file

from keyboards.inline_operators_markup import Operator_keyboard
from keyboards.inline_start_survey import Survey_inlines_keyboards
from keyboards.inline_initiate import yes_no_keyboard
from keyboards.all_keyboards import all_keyboards

from transliterate import translit

from mailing.mailing import send_vacation_email


# @dp.message_handler(content_types='text', state=None)
async def recognizing(message: types.Message):
    response_id = recognize_question(message.text, question_list)
    if response_id:
        answer = db.find_answer_by_question_id(response_id)
    else:
        answer = db.no_answer()

    check_keyboards = is_reply_keyboard(answer)
    if len(check_keyboards) == 1:
        await message.reply(is_breakes(check_keyboards[0]))
    else:
        keyboard = all_keyboards[check_keyboards[-1]]
        await message.reply(is_breakes(check_keyboards[0]), reply_markup=keyboard)


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


# Состояния для поиска сотрудника --------------------------------------------------------------------------------------
class FSM_search(StatesGroup):
    enter_name = State()
    enter_surname = State()
    enter_patronymic = State()
    enter_email = State()
    enter_tg_nickname = State()
    enter_department = State()
    enter_title = State()


# @dp.callback_query_handler(lambda c: c.data.startswith("search"), state=None)
async def search(callback_query: types.CallbackQuery, state: FSMContext):
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
    async with state.proxy() as data:
        data["answer"] = answer.message_id


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
        await bot.edit_message_text(text=f"<u>Вот кого удалось найти:</u>\n\n{text}\n", chat_id=message.from_id,
                                    message_id=last_answer, parse_mode="html")
        await state.finish()
    else:
        await bot.edit_message_text(f"Я не нашел никого с именем {message.text} T_T", chat_id=message.from_id,
                                    message_id=last_answer, parse_mode=types.ParseMode.HTML)
        partial_search_result = db.partial_search_by_name(message.text)
        if partial_search_result:
            text = ''
            for i in partial_search_result:
                text += search_message(i["id"], i["first_name"], i["surname"], i["job_title"])
            await message.answer(text=f"<u>Вот кто частично подходит под твой запрос:</u>\n\n{text}\n",
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
        await bot.edit_message_text(text=f"<u>Вот кого удалось найти:</u>\n\n{text}\n", chat_id=message.from_id,
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
            await message.answer(text=f"<u>Вот кто частично подходит под твой запрос:</u>\n\n{text}\n",
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
        await bot.edit_message_text(text=f"<u>Вот кого удалось найти:</u>\n\n{text}\n", chat_id=message.from_id,
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
            await message.answer(text=f"<u>Вот кто частично подходит под твой запрос:</u>\n\n{text}\n",
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
        await bot.edit_message_text(text=f"<u>Вот кого удалось найти:</u>\n\n{text}\n", chat_id=message.from_id,
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
            await message.answer(text=f"<u>Вот кто частично подходит под твой запрос:</u>\n\n{text}\n",
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
        await bot.edit_message_text(text=f"<u>Вот кого удалось найти:</u>\n\n{text}\n",
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
            await message.answer(text=f"<u>Вот кто частично подходит под твой запрос:</u>\n\n{text}\n",
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
        await bot.edit_message_text(text=f"<u>Вот кого удалось найти:</u>\n\n{text}\n",
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
            await message.answer(text=f"<u>Вот кто частично подходит под твой запрос:</u>\n\n{text}\n",
                                 parse_mode=types.ParseMode.HTML)
        await state.finish()


@dp.message_handler(content_types='text', state=FSM_search.enter_department)
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
        await bot.edit_message_text(text=f"<u>Вот что удалось найти:</u>\n\n{text}\n",
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
            await message.answer(text=f"<u>Вот кто частично подходит под твой запрос:</u>\n\n{text}\n",
                                 parse_mode=types.ParseMode.HTML)
        await state.finish()


# @dp.message_handler(content_types='video')
async def got_video(message: types.Message):
    await message.answer(f"Получил видео. Его id {message.video.file_id}")


# Состояния для опросника при старте работы ----------------------------------------------------------------------------
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
        await callback_query.message.answer(message_dict["help"])


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
    await callback_query.message.answer(message_dict["help"])


# Состояния для заполнения анкеты новичком -----------------------------------------------------------------------------
class FSM_newbie_questioning(StatesGroup):
    newbie_questioning_start = State()
    asking_surname = State()
    email_creating = State()
    asking_surname_eng = State()
    asking_bday = State()
    asking_phone = State()
    asking_email = State()
    asking_photo = State()
    asking_hobby = State()
    commit_data = State()
    show_video = State()


# @dp.callback_query_handler(lambda c: c.data == "start",
#                            state=FSM_newbie_questioning.newbie_questioning_start)
async def questioning_start(callback_query: types.CallbackQuery, state: FSMContext):
    msg_todel = await callback_query.message.answer("Введи свое ФИО (Например Пупкин Иван Александрович):")
    async with state.proxy() as data:
        data["to_delete"] = []
        data["to_delete"].append(msg_todel.message_id)
    await FSM_newbie_questioning.next()


# @dp.message_handler(state=FSM_newbie_questioning.asking_surname)
async def load_surname(message: types.Message, state: FSMContext):
    name = message.text.split(" ")[1]
    surname = message.text.split(" ")[0]
    patronymic = message.text.split(" ")[2]

    await FSM_newbie_questioning.next()
    keyboard = Survey_inlines_keyboards()
    msg_todel = await message.answer("Я правильно написал твою фамилию на английском ?:\n "
                                     f"<b>{translit(surname, language_code='ru', reversed=True)}</b>\n"
                                     "Эта формулировка будет использована в создании почты", parse_mode="html",
                                     reply_markup=keyboard.is_ok())
    async with state.proxy() as data:
        data["name"] = name
        data["patronymic"] = patronymic
        data["surname"] = surname
        data["to_delete"].append(msg_todel.message_id)
        data["to_delete"].append(message.message_id)


# @dp.callback_query_handler(lambda c: c.data.startswith("answer"),
#                            state=FSM_newbie_questioning.email_creating)
async def email_confirming(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data.split(" ")[1] == "correct":
        msg_todel = await bot.send_message(callback_query.from_user.id,
                                           "Введи свою дату рождения (формат dd.mm.yyyy): ")
        await FSM_newbie_questioning.asking_bday.set()
        async with state.proxy() as data:
            data["surname_eng"] = translit(data["surname"], language_code='ru', reversed=True)
            data["to_delete"].append(msg_todel.message_id)
    else:
        await FSM_newbie_questioning.asking_surname_eng.set()
        msg_todel = await bot.send_message(callback_query.from_user.id, "Ок, тогда введи фамилию на английском:")
        async with state.proxy() as data:
            data["to_delete"].append(msg_todel.message_id)


# @dp.message_handler(state=FSM_newbie_questioning.asking_surname_eng)
async def load_eng_surname(message: types.Message, state: FSMContext):
    await FSM_newbie_questioning.next()
    msg_todel = await message.answer("Введи свою дату рождения (формат dd.mm.yyyy): ")
    async with state.proxy() as data:
        data["surname_eng"] = message.text
        data["to_delete"].append(msg_todel.message_id)
        data["to_delete"].append(message.message_id)


# @dp.message_handler(state=FSM_newbie_questioning.asking_bday)
async def load_bdate(message: types.Message, state: FSMContext):
    # todo сделать валидатор для даты формат dd.mm.yyyy
    await FSM_newbie_questioning.next()
    msg_todel = await message.answer("Теперь введи свой телефон для связи (формат 7 ХХХ ХХХ ХХХХ): ")
    async with state.proxy() as data:
        data["bdate"] = message.text
        data["to_delete"].append(msg_todel.message_id)
        data["to_delete"].append(message.message_id)


# @dp.message_handler(state=FSM_newbie_questioning.asking_phone)
async def load_phone(message: types.Message, state: FSMContext):
    # todo сделать валидатор для телефона формат 7 ХХХ ХХХ ХХХХ
    await FSM_newbie_questioning.next()
    msg_todel = await message.answer("Укажи свой e-mail (для отправки документов): ")
    async with state.proxy() as data:
        data["phone"] = message.text
        data["to_delete"].append(msg_todel.message_id)
        data["to_delete"].append(message.message_id)


# @dp.message_handler(state=FSM_newbie_questioning.asking_email)
async def load_email(message: types.Message, state: FSMContext):
    # todo сделать валидатор для email формат {name}@{domen}.{restr}
    await FSM_newbie_questioning.next()
    msg_todel = await message.answer("Загрузи свое фото (просто перетащи фото сюда): ")
    async with state.proxy() as data:
        data["email"] = message.text
        data["to_delete"].append(msg_todel.message_id)
        data["to_delete"].append(message.message_id)


# @dp.message_handler(content_types="photo", state=FSM_newbie_questioning.asking_photo)
async def load_photo(message: types.Message, state: FSMContext):
    await FSM_newbie_questioning.next()
    msg_todel = await message.answer("Расскажи о своих хобби увлечениях: ")
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id
        data["to_delete"].append(msg_todel.message_id)
        data["to_delete"].append(message.message_id)


# @dp.message_handler(state=FSM_newbie_questioning.asking_hobby)
async def load_hobby(message: types.Message, state: FSMContext):
    keyboard = Survey_inlines_keyboards()
    async with state.proxy() as data:
        data["hobby"] = message.text
    await FSM_newbie_questioning.next()
    await bot.delete_message(message.from_id, message.message_id)
    for i in data["to_delete"]:
        await bot.delete_message(message.from_id, i)
    await message.answer_photo(data["photo"], 'Проверим что получилось:\n\n'
                                              f'{data["surname"]} {data["name"]} {data["patronymic"]}\n'
                                              f'Дата рождения: {data["bdate"]}\n'
                                              f'Телефон: +{data["phone"]}\n'
                                              f'E-mail: {data["email"]}\n'
                                              f'Хобби и увлечения: {data["hobby"]}')
    buttons_to_remove = await message.answer("Все верно ?", reply_markup=keyboard.is_ok())
    async with state.proxy() as data:
        data["buttons_to_remove"] = buttons_to_remove.message_id


# @dp.callback_query_handler(lambda c: c.data.startswith("answer"), state=FSM_newbie_questioning.commit_data)
async def commit_data(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard = Survey_inlines_keyboards()
    if callback_query.data.split(" ")[1] == "correct":
        operator_keyboard = Operator_keyboard()
        async with state.proxy() as data:
            await bot.send_photo(operator_list[0], data["photo"], 'Нужно проверить нового пользователя:\n\n'
                                                                  f'{data["surname"]} {data["name"]} {data["patronymic"]}\n'
                                                                  f'Дата рождения: {data["bdate"]}\n'
                                                                  f'Телефон: +{data["phone"]}\n'
                                                                  f'E-mail: {data["email"]}\n'
                                                                  f'Хобби и увлечения: {data["hobby"]}',
                                 reply_markup=operator_keyboard.confirm_new_user())
        await FSM_newbie_questioning.next()
        await bot.edit_message_text("Данные отправлены на обработку модератору",
                                    callback_query.from_user.id,
                                    data["buttons_to_remove"])
        await bot.send_message(callback_query.from_user.id, "Cейчас потребуется 2 минуты концентрации."
                                                            "Мы расскажем в видеоролике, кто такие ТИМ ФОРСЕРЫ и "
                                                            "кому куда писать по каким вопросам. Начнем ?",
                               reply_markup=keyboard.ok_keyboard())
    else:
        await FSM_newbie_questioning.newbie_questioning_start.set()
        async with state.proxy() as data:
            data["to_delete"] = []
        await bot.send_message(callback_query.from_user.id, "Введи свое ФИО (Например Пупкин Иван Александрович):")
        await FSM_newbie_questioning.next()


# @dp.callback_query_handler(lambda c: c.data == "start", state=FSM_newbie_questioning.show_video)
async def show_video(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard = Survey_inlines_keyboards()
    await state.finish()
    await bot.send_video(callback_query.from_user.id, message_dict["greeting_video_id"])
    await bot.send_message(callback_query.from_user.id,
                           "Теперь у тебя побольше представлений о работе ТИМ ФОРС?\n"
                           "Готов пройти короткий опрос ?",
                           reply_markup=keyboard.start_survey())


# Состояния для пересылки письма об отпуске ----------------------------------------------------------------------------
class FSM_send_vacation_email(StatesGroup):
    enter_vacation_period = State()
    is_agreed = State()
    send_doc = State()
    enter_coordinator = State()


# @dp.callback_query_handler(lambda c: c.data.startswith("initiate"), state=None)
async def initiate_vacation_email(callback_query: types.CallbackQuery, state=None):
    await callback_query.answer()
    sender_tg_id = callback_query.from_user.id
    sender = db.find_contacts_by_tg_id(sender_tg_id)
    async with state.proxy() as data:
        data["from_tg_id"] = sender_tg_id
        data["from_name"] = sender["first_name"]
        data["from_surname"] = sender["surname"]
        data["job_title"] = sender["job_title"]
    await FSM_send_vacation_email.enter_vacation_period.set()
    await bot.send_message(chat_id=callback_query.from_user.id, text="В какие сроки планируется отпуск?: ")


# @dp.message_handler(state=FSM_send_vacation_email.enter_vacation_period)
async def save_vacaton_period(message: types.Message, state=FSMContext):
    await FSM_send_vacation_email.is_agreed.set()
    async with state.proxy() as data:
        data["vacation_period"] = message.text
    await bot.send_message(chat_id=message.from_user.id, text="Отпуск согласован с руководителем?: ",
                           reply_markup=yes_no_keyboard)


# @dp.callback_query_handler(lambda c: c.data.startswith("answer"), state=FSM_send_vacation_email.is_agreed)
async def save_is_agreed(callback_query: types.CallbackQuery, state=FSMContext):
    await callback_query.answer()
    await FSM_send_vacation_email.send_doc.set()
    async with state.proxy() as data:
        data["is_agreed"] = callback_query.data.split(" ")[1]
    await bot.send_message(chat_id=callback_query.from_user.id, text="Пришлите фото заполненного заявления: ")


# @dp.message_handler(content_types="photo", state=FSM_send_vacation_email.send_doc)
async def save_doc(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        await FSM_send_vacation_email.enter_coordinator.set()
        destination = os.getcwd() + "/temp_saves/" + data["from_name"] + " " + data["from_surname"] + ".jpg"
        data["image_path"] = destination
        await message.photo[-1].download(destination_file=destination)
    await bot.send_message(chat_id=message.from_user.id, text="Кто ваш координатор в ТИМ ФОРС: ")


# @dp.message_handler(state=FSM_send_vacation_email.enter_coordinator)
async def save_coordinator(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["coordinator"] = message.text
    from_name = data["from_name"]
    from_surname = data["from_surname"]
    job_title = data["job_title"]
    vacation_period = data["vacation_period"]
    is_agreed = data["is_agreed"]
    coordinator_name = data["coordinator"]
    image_path = data["image_path"]
    is_ok = asyncio.create_task(send_vacation_email(from_name, from_surname, job_title, vacation_period, is_agreed,
                                                    coordinator_name, image_path))
    if is_ok:
        text = f"Ваше заявление на отпуск в период {data['vacation_period']} отправлено координатору"
        await asyncio.sleep(10)
        await asyncio.create_task(delete_temp_file(data["image_path"]))
    else:
        text = is_ok
    await bot.send_message(chat_id=message.from_user.id, text=text)
    await state.finish()


def register_handlers_other(dp: Dispatcher):
    dp.register_callback_query_handler(get_document, lambda c: c.data.startswith("get"), state=None)
    dp.register_message_handler(recognizing, content_types='text', state=None)

    dp.register_callback_query_handler(search, lambda c: c.data.startswith("search"), state=None)
    dp.register_message_handler(search_by_surname_step2, content_types='text', state=FSM_search.enter_surname)
    dp.register_message_handler(search_by_title_step2, content_types='text', state=FSM_search.enter_title)
    dp.register_message_handler(search_by_name_step2, content_types='text', state=FSM_search.enter_name)
    dp.register_message_handler(search_by_patronymic_step2, content_types='text', state=FSM_search.enter_patronymic)
    dp.register_message_handler(search_by_tg_nickname_step2, content_types='text', state=FSM_search.enter_tg_nickname)
    dp.register_message_handler(search_by_email_step2, content_types='text', state=FSM_search.enter_email)

    dp.register_message_handler(got_video, content_types='video')

    dp.register_callback_query_handler(first_question, lambda c: c.data.startswith("survey"), state=None)
    dp.register_callback_query_handler(second_question, lambda c: c.data.startswith("first"),
                                       state=FSM_start_survey.second_question)
    dp.register_callback_query_handler(third_question, lambda c: c.data.startswith("second"),
                                       state=FSM_start_survey.third_question)
    dp.register_callback_query_handler(answers, lambda c: c.data.startswith("third"),
                                       state=FSM_start_survey.compare_answers)

    dp.register_callback_query_handler(questioning_start, lambda c: c.data == "start",
                                       state=FSM_newbie_questioning.newbie_questioning_start)
    dp.register_message_handler(load_surname, state=FSM_newbie_questioning.asking_surname)
    dp.register_callback_query_handler(email_confirming, lambda c: c.data.startswith("answer"),
                                       state=FSM_newbie_questioning.email_creating)
    dp.register_message_handler(load_eng_surname, state=FSM_newbie_questioning.asking_surname_eng)
    dp.register_message_handler(load_bdate, state=FSM_newbie_questioning.asking_bday)
    dp.register_message_handler(load_phone, state=FSM_newbie_questioning.asking_phone)
    dp.register_message_handler(load_email, state=FSM_newbie_questioning.asking_email)
    dp.register_message_handler(load_photo, content_types="photo", state=FSM_newbie_questioning.asking_photo)
    dp.register_message_handler(load_hobby, state=FSM_newbie_questioning.asking_hobby)
    dp.register_callback_query_handler(commit_data,
                                       lambda c: c.data.startswith("answer"), state=FSM_newbie_questioning.commit_data)
    dp.register_callback_query_handler(show_video, lambda c: c.data == "start", state=FSM_newbie_questioning.show_video)

    dp.register_callback_query_handler(initiate_vacation_email, lambda c: c.data.startswith("initiate"), state=None)
    dp.register_message_handler(save_vacaton_period, state=FSM_send_vacation_email.enter_vacation_period)
    dp.register_callback_query_handler(save_is_agreed,
                                       lambda c: c.data.startswith("answer"), state=FSM_send_vacation_email.is_agreed)
    dp.register_message_handler(save_doc, content_types="photo", state=FSM_send_vacation_email.send_doc)
    dp.register_message_handler(save_coordinator, state=FSM_send_vacation_email.enter_coordinator)
