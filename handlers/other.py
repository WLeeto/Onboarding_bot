import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot, db
from dicts.messages import sleep_timer
from func.all_func import question_list, delete_message

from func.all_func import recognize_question


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


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(recognizing, content_types='text', state=None)
    dp.register_callback_query_handler(search_by_surname_step1, lambda c: c.data == "search_by_name", state=None)
    dp.register_message_handler(search_by_surname_step2, content_types='text', state=FSM_search_by_name.enter_surname)
    dp.register_callback_query_handler(search_by_title_step1, lambda c: c.data == "search_by_title", state=None)
    dp.register_message_handler(search_by_title_step2, content_types='text', state=FSM_search_by_title.enter_title)
