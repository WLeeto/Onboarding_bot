import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot, db
from dicts.messages import sleep_timer, start_survey_dict, message_dict
from func.all_func import question_list, delete_message, recognize_question, start_survey_answers

from keyboards.inline_start_survey import Survey_inlines_keyboards


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
                                    message_id=callback_query.message.message_id,)
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

