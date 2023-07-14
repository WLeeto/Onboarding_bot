from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from create_bot import dp, db, bot
from func.all_func import search_message, delete_message, create_find_answer_if_found, create_find_answer_if_not_found

from States.states import FSM_search


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
        text = ""
        for i in result:
            text += search_message(i.id, i.first_name, i.surname, i.middle_name, i.job_title, i.tg_name)
    else:
        text = f"Я не смог никого найти T_T, скорее всего пользователя с таким номером в базе нет"
    await state.finish()
    await delete_message(message, 0)
    await bot.edit_message_text(text, chat_id=message.from_id, message_id=last_answer, parse_mode=types.ParseMode.HTML,
                                disable_web_page_preview=True)


# @dp.message_handler(content_types='text', state=FSM_search.enter_name)
async def search_by_name_step2(message: types.Message, state: FSMContext):
    result = db.find_by_name(message.text)
    await message.delete()
    async with state.proxy() as data:
        last_answer = data["answer"]
    if result:
        await create_find_answer_if_found(result, last_answer, message)
    else:
        partial_search_result = db.partial_search_by_name(message.text)
        await create_find_answer_if_not_found(partial_search_result, last_answer, message, 'именем')

    await state.finish()


# @dp.message_handler(content_types='text', state=FSM_search.enter_surname)
async def search_by_surname_step2(message: types.Message, state: FSMContext):
    result = db.find_by_surname(message.text)
    await message.delete()
    async with state.proxy() as data:
        last_answer = data["answer"]
    if result:
        await create_find_answer_if_found(result, last_answer, message)
    else:
        partial_search_result = db.partial_search_by_surname(message.text)
        await create_find_answer_if_not_found(partial_search_result, last_answer, message, 'фамилией')

    await state.finish()


# @dp.message_handler(content_types='text', state=FSM_search.enter_patronymic)
async def search_by_patronymic_step2(message: types.Message, state: FSMContext):
    result = db.find_by_patronymic(message.text)
    await message.delete()
    async with state.proxy() as data:
        last_answer = data["answer"]
    if result:
        await create_find_answer_if_found(result, last_answer, message)
    else:
        partial_search_result = db.partial_search_by_patronymic(message.text)
        await create_find_answer_if_not_found(partial_search_result, last_answer, message, 'отчеством')

    await state.finish()


# @dp.message_handler(content_types='text', state=FSM_search.enter_title)
async def search_by_title_step2(message: types.Message, state: FSMContext):
    result = db.find_by_title(message.text)
    await message.delete()
    async with state.proxy() as data:
        last_answer = data["answer"]
    if result:
        await create_find_answer_if_found(result, last_answer, message)
    else:
        partial_search_result = db.partial_search_by_title(message.text)
        await create_find_answer_if_not_found(partial_search_result, last_answer, message, 'должностью')

    await state.finish()


# @dp.message_handler(content_types='text', state=FSM_search.enter_tg_nickname)
async def search_by_tg_nickname_step2(message: types.Message, state: FSMContext):
    result = db.find_by_telegram_ninckname(message.text)
    await message.delete()
    async with state.proxy() as data:
        last_answer = data["answer"]
    if result:
        await create_find_answer_if_found(result, last_answer, message)
    else:
        partial_search_result = db.partial_search_by_telegram_ninckname(message.text)
        await create_find_answer_if_not_found(partial_search_result, last_answer, message, 'ником')

    await state.finish()


# @dp.message_handler(content_types='text', state=FSM_search.enter_email)
async def search_by_email_step2(message: types.Message, state: FSMContext):
    result = db.find_by_email(message.text)
    await message.delete()
    async with state.proxy() as data:
        last_answer = data["answer"]
    if result:
        await create_find_answer_if_found(result, last_answer, message)
    else:
        partial_search_result = db.partial_search_by_email(message.text)
        await create_find_answer_if_not_found(partial_search_result, last_answer, message, 'почтой')

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
            employers = "\n".join(i['employers'])
            text += f"<b>{i['name']}:</b>\n" \
                    f"<b>Сотрудники:</b>\n" \
                    f"{employers}\n\n"
        await bot.edit_message_text(text=f"<u>Вот, что удалось найти:</u>\n\n{text}\n",
                                    chat_id=message.from_id, message_id=last_answer, parse_mode=types.ParseMode.HTML,
                                    disable_web_page_preview=True)
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
                        f"{employers}\n\n"
            await message.answer(text=f"<u>Вот, кто частично подходит под твой запрос:</u>\n\n{text}\n",
                                 parse_mode=types.ParseMode.HTML,
                                 disable_web_page_preview=True)
        await state.finish()

# Пример пагинации -----------------------------------------------------------------------------------------------------

button1 = InlineKeyboardButton(text="Next", callback_data="pagi next")
button2 = InlineKeyboardButton(text="Prev", callback_data="pagi prev")
button3 = InlineKeyboardButton(text="Exit", callback_data="pagi exit")
pagi_kb = InlineKeyboardMarkup(row_width=2).add(button2, button1, button3)
only_back_kb = InlineKeyboardMarkup(row_width=1).add(button2, button3)
only_next_kb = InlineKeyboardMarkup(row_width=1).add(button1, button3)


class FSM_pagi(StatesGroup):
    paginator = State()


@dp.message_handler(commands="pg")
async def paginator_test(message: types.Message, state: FSMContext):
    await FSM_pagi.paginator.set()
    temp_list = db.partial_search_by_name("ол")
    text = ""
    async with state.proxy() as data:
        data["pagi"] = 1
    i = temp_list[0]
    text += search_message(i.id, i.first_name, i.surname, i.middle_name, i.job_title, i.tg_name)
    await message.answer(text, parse_mode=types.ParseMode.HTML, reply_markup=only_next_kb)


@dp.callback_query_handler(lambda c: c.data.startswith("pagi"), state=FSM_pagi.paginator)
async def pagi(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data.split(" ")[1] == "next":
        async with state.proxy() as data:
            data["pagi"] += 1
            if len(contacts_dict(db.partial_search_by_name("ол"))) > data["pagi"]:
                keyboard = pagi_kb
            else:
                keyboard = only_back_kb
            next_contact = contacts_dict(db.partial_search_by_name("ол"))[data["pagi"]]
            text = search_message(next_contact.id, next_contact.first_name, next_contact.surname,
                                  next_contact.middle_name, next_contact.job_title, next_contact.tg_name)
            await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
            await callback_query.answer()
    elif callback_query.data.split(" ")[1] == "prev":
        async with state.proxy() as data:
            data["pagi"] -= 1
            if data["pagi"] != 1:
                keyboard = pagi_kb
            else:
                keyboard = only_next_kb
            prev_contact = contacts_dict(db.partial_search_by_name("ол"))[data["pagi"]]
            text = search_message(prev_contact.id, prev_contact.first_name, prev_contact.surname,
                                  prev_contact.middle_name, prev_contact.job_title, prev_contact.tg_name)
        await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        await callback_query.answer()
    elif callback_query.data.split(" ")[1] == "exit":
        await state.finish()
        await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id,
                                            reply_markup=None)
        await callback_query.answer()


def contacts_dict(contacts: list) -> dict:
    result = {}
    page = 1
    for i in contacts:
        result[page] = i
        page += 1
    return result

# ----------------------------------------------------------------------------------------------------------------------


def register_handlers_find(dp: Dispatcher):
    dp.register_callback_query_handler(search, lambda c: c.data.startswith("search"), state=None)
    dp.register_message_handler(search_by_surname_step2, content_types='text', state=FSM_search.enter_surname)
    dp.register_message_handler(search_by_title_step2, content_types='text', state=FSM_search.enter_title)
    dp.register_message_handler(search_by_name_step2, content_types='text', state=FSM_search.enter_name)
    dp.register_message_handler(search_by_patronymic_step2, content_types='text', state=FSM_search.enter_patronymic)
    dp.register_message_handler(search_by_tg_nickname_step2, content_types='text',
                                state=FSM_search.enter_tg_nickname)
    dp.register_message_handler(search_by_email_step2, content_types='text', state=FSM_search.enter_email)
    dp.register_message_handler(search_by_department_step2, content_types='text', state=FSM_search.enter_department)
    dp.register_message_handler(search_by_phone_step2, content_types="text", state=FSM_search.enter_phone)
