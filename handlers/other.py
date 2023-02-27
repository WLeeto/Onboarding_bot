import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot, db
from dicts.messages import sleep_timer, start_survey_dict, message_dict, operator_list
from func.all_func import question_list, delete_message, recognize_question, start_survey_answers
from keyboards.inline_operators_markup import Operator_keyboard

from keyboards.inline_start_survey import Survey_inlines_keyboards

from transliterate import translit


# @dp.message_handler(content_types='text', state=None)
async def recognizing(message: types.Message):
    response_id = recognize_question(message.text, question_list)
    if response_id:
        answer = db.find_answer_by_question_id(response_id)
    else:
        answer = db.no_answer()
    await message.reply(answer)


# Состояния для поиска сотрудника по фамилии ---------------------------------------------------------------------------
class FSM_search_by_name(StatesGroup):
    enter_surname = State()


# @dp.callback_query_handler(lambda c: c.data == "search_by_name", state=None)
async def search_by_surname_step1(callback_query: types.CallbackQuery):
    await FSM_search_by_name.enter_surname.set()
    answer = await bot.edit_message_text("Кого ищем ? (введи фамилию):",
                                         callback_query.from_user.id, callback_query.message.message_id)
    asyncio.create_task(delete_message(answer, sleep_timer))


# @dp.message_handler(content_types='text', state=FSM_search_by_name.enter_surname)
async def search_by_surname_step2(message: types.Message, state: FSMContext):
    async with state.proxy() as surname:
        surname['surname'] = message.text
    result = db.find_by_surname(surname['surname'])
    await message.delete()
    if result:
        text = ''
        for i in result:
            contacts = db.find_contacts_by_id(i["id"])
            contacts_text = f"  <b>E-mail:</b> {contacts.get('e-mail')}\n" \
                            f"  <b>Phone:</b> {contacts.get('phone')}"
            text += f"<b>Имя:</b> {i['first_name']}\n" \
                    f"<b>Фамилия</b>: {i['surname']}\n" \
                    f"<b>Должность</b>: {i['job_title']}\n" \
                    f"<b>Отдел:</b> {db.find_department_by_user_id(i['id'])}\n" \
                    f"<b>Контакты:</b> \n{contacts_text}\n\n"
        await message.answer(text=f"<u>Вот кого удалось найти:</u>\n\n{text}\n", parse_mode="html")
        await state.finish()
    else:
        await message.answer(f"Я не нашел никого с фамилией {message.text} T_T")
        await state.finish()


# Состояния для поиска сотрудника по должности -------------------------------------------------------------------------
class FSM_search_by_title(StatesGroup):
    enter_title = State()


# @dp.callback_query_handler(lambda c: c.data == "search_by_title", state=None)
async def search_by_title_step1(callback_query: types.CallbackQuery):
    await FSM_search_by_title.enter_title.set()
    answer = await bot.edit_message_text("Кого ищем ? (введите должность)",
                                         callback_query.from_user.id, callback_query.message.message_id)
    asyncio.create_task(delete_message(answer, sleep_timer))


# @dp.message_handler(content_types='text', state=FSM_search_by_title.enter_title)
async def search_by_title_step2(message: types.Message, state: FSMContext):
    async with state.proxy() as title:
        title['title'] = message.text
    result = db.find_by_title(title['title'])
    await message.delete()
    if result:
        text = ''
        for i in result:
            contacts = db.find_contacts_by_id(i["id"])
            contacts_text = f"  <b>E-mail:</b> {contacts.get('e-mail')}\n" \
                            f"  <b>Phone:</b> {contacts.get('phone')}"
            text += f"<b>Имя:</b> {i['first_name']}\n" \
                    f"<b>Фамилия</b>: {i['surname']}\n" \
                    f"<b>Должность</b>: {i['job_title']}\n" \
                    f"<b>Отдел:</b> {db.find_department_by_user_id(i['id'])}\n" \
                    f"<b>Контакты:</b> \n{contacts_text}\n\n"
        await message.answer(text=f"<u>Вот кого удалось найти:</u>\n\n{text}\n", parse_mode="html")
        await state.finish()
    else:
        await message.answer(f"Я не нашел никого с должностью {message.text} T_T")
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


@dp.callback_query_handler(lambda c: c.data == "start",
                           state=FSM_newbie_questioning.newbie_questioning_start)
async def questioning_start(callback_query: types.CallbackQuery, state: FSMContext):
    msg_todel = await callback_query.message.answer("Введи свое ФИО (Например Пупкин Иван Александрович):")
    async with state.proxy() as data:
        data["to_delete"] = []
        data["to_delete"].append(msg_todel.message_id)
    await FSM_newbie_questioning.next()


@dp.message_handler(state=FSM_newbie_questioning.asking_surname)
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


@dp.callback_query_handler(lambda c: c.data.startswith("answer"),
                           state=FSM_newbie_questioning.email_creating)
async def email_confirming(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data.split(" ")[1] == "correct":
        msg_todel = await bot.send_message(callback_query.from_user.id, "Введи свою дату рождения (формат dd.mm.yyyy): ")
        await FSM_newbie_questioning.asking_bday.set()
        async with state.proxy() as data:
            data["surname_eng"] = translit(data["surname"], language_code='ru', reversed=True)
            data["to_delete"].append(msg_todel.message_id)
    else:
        await FSM_newbie_questioning.asking_surname_eng.set()
        msg_todel = await bot.send_message(callback_query.from_user.id, "Ок, тогда введи фамилию на английском:")
        async with state.proxy() as data:
            data["to_delete"].append(msg_todel.message_id)


@dp.message_handler(state=FSM_newbie_questioning.asking_surname_eng)
async def load_eng_surname(message: types.Message, state: FSMContext):
    await FSM_newbie_questioning.next()
    msg_todel = await message.answer("Введи свою дату рождения (формат dd.mm.yyyy): ")
    async with state.proxy() as data:
        data["surname_eng"] = message.text
        data["to_delete"].append(msg_todel.message_id)
        data["to_delete"].append(message.message_id)


@dp.message_handler(state=FSM_newbie_questioning.asking_bday)
async def load_bdate(message: types.Message, state: FSMContext):
    # todo сделать валидатор для даты формат dd.mm.yyyy
    await FSM_newbie_questioning.next()
    msg_todel = await message.answer("Теперь введи свой телефон для связи (формат 7 ХХХ ХХХ ХХХХ): ")
    async with state.proxy() as data:
        data["bdate"] = message.text
        data["to_delete"].append(msg_todel.message_id)
        data["to_delete"].append(message.message_id)


@dp.message_handler(state=FSM_newbie_questioning.asking_phone)
async def load_phone(message: types.Message, state: FSMContext):
    # todo сделать валидатор для телефона формат 7 ХХХ ХХХ ХХХХ
    await FSM_newbie_questioning.next()
    msg_todel = await message.answer("Укажи свой e-mail (для отправки документов): ")
    async with state.proxy() as data:
        data["phone"] = message.text
        data["to_delete"].append(msg_todel.message_id)
        data["to_delete"].append(message.message_id)


@dp.message_handler(state=FSM_newbie_questioning.asking_email)
async def load_email(message: types.Message, state: FSMContext):
    # todo сделать валидатор для email формат {name}@{domen}.{restr}
    await FSM_newbie_questioning.next()
    msg_todel = await message.answer("Загрузи свое фото (просто перетащи фото сюда): ")
    async with state.proxy() as data:
        data["email"] = message.text
        data["to_delete"].append(msg_todel.message_id)
        data["to_delete"].append(message.message_id)


@dp.message_handler(content_types="photo", state=FSM_newbie_questioning.asking_photo)
async def load_photo(message: types.Message, state: FSMContext):
    await FSM_newbie_questioning.next()
    msg_todel = await message.answer("Расскажи о своих хобби увлечениях: ")
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id
        data["to_delete"].append(msg_todel.message_id)
        data["to_delete"].append(message.message_id)


@dp.message_handler(state=FSM_newbie_questioning.asking_hobby)
async def load_hobby(message: types.Message, state: FSMContext):
    keyboard = Survey_inlines_keyboards()
    async with state.proxy() as data:
        data["hobby"] = message.text
    await FSM_newbie_questioning.next()
    await bot.delete_message(message.from_id, message.message_id)
    for i in data["to_delete"]:
        await bot.delete_message(message.from_id, i)
        data["to_delete"].remove(i)
    await message.answer_photo(data["photo"], 'Проверим что получилось:\n\n'
                                              f'{data["surname"]} {data["name"]} {data["patronymic"]}\n'
                                              f'Дата рождения: {data["bdate"]}\n'
                                              f'Телефон: +{data["phone"]}\n'
                                              f'E-mail: {data["email"]}\n'
                                              f'Хобби и увлечения: {data["hobby"]}',
                               reply_markup=keyboard.is_ok())


@dp.callback_query_handler(lambda c: c.data.startswith("answer"), state=FSM_newbie_questioning.commit_data)
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
        await bot.send_message(callback_query.from_user.id, "Данные отправлены на обработку модератору")
        await bot.send_message(callback_query.from_user.id, "Cейчас потребуется 2 минуты концентрации."
                                                            "Мы расскажем в видеоролике, кто такие ТИМ ФОРСЕРЫ и "
                                                            "кому куда писать по каким вопросам. Начнем ?",
                               reply_markup=keyboard.ok_keyboard())
    else:
        await FSM_newbie_questioning.newbie_questioning_start.set()
        await bot.send_message(callback_query.from_user.id, "Введи свое ФИО (Например Пупкин Иван Александрович):")
        await FSM_newbie_questioning.next()


@dp.callback_query_handler(lambda c: c.data == "start", state=FSM_newbie_questioning.show_video)
async def show_video(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard = Survey_inlines_keyboards()
    await state.finish()
    await bot.send_video(callback_query.from_user.id, message_dict["greeting_video_id"])
    await bot.send_message(callback_query.from_user.id,
                           "Теперь у тебя побольше представлений о работе ТИМ ФОРС?\n"
                           "Готов пройти короткий опрос ?",
                           reply_markup=keyboard.start_survey())


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(recognizing, content_types='text', state=None)
    dp.register_callback_query_handler(search_by_surname_step1, lambda c: c.data == "search_by_name", state=None)
    dp.register_message_handler(search_by_surname_step2, content_types='text', state=FSM_search_by_name.enter_surname)
    dp.register_callback_query_handler(search_by_title_step1, lambda c: c.data == "search_by_title", state=None)
    dp.register_message_handler(search_by_title_step2, content_types='text', state=FSM_search_by_title.enter_title)
    dp.register_message_handler(got_video, content_types='video')

    dp.register_callback_query_handler(first_question, lambda c: c.data.startswith("survey"), state=None)
    dp.register_callback_query_handler(second_question, lambda c: c.data.startswith("first"),
                                       state=FSM_start_survey.second_question)
    dp.register_callback_query_handler(third_question, lambda c: c.data.startswith("second"),
                                       state=FSM_start_survey.third_question)
    dp.register_callback_query_handler(answers, lambda c: c.data.startswith("third"),
                                       state=FSM_start_survey.compare_answers)
