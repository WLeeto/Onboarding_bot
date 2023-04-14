from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from create_bot import db, bot
from func.all_func import search_message, delete_message

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
            text += search_message(i.id, i.first_name, i.surname, i.middle_name, i.job_title, i.tg_name)
        await bot.edit_message_text(text=f"<u>Вот, кого удалось найти:</u>\n\n{text}\n", chat_id=message.from_id,
                                    message_id=last_answer, parse_mode=types.ParseMode.HTML)
    else:
        await bot.edit_message_text(f"Я не нашел никого с именем {message.text} T_T", chat_id=message.from_id,
                                    message_id=last_answer, parse_mode=types.ParseMode.HTML)
        partial_search_result = db.partial_search_by_name(message.text)
        if partial_search_result:
            text = ''
            for i in partial_search_result:
                text += search_message(i.id, i.first_name, i.surname, i.middle_name, i.job_title, i.tg_name)
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
            text += search_message(i.id, i.first_name, i.surname, i.middle_name, i.job_title, i.tg_name)
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
                text += search_message(i.id, i.first_name, i.surname, i.middle_name, i.job_title, i.tg_name)
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
            text += search_message(i.id, i.first_name, i.surname, i.middle_name, i.job_title, i.tg_name)
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
                text += search_message(i.id, i.first_name, i.surname, i.middle_name, i.job_title, i.tg_name)
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
            text += search_message(i.id, i.first_name, i.surname, i.middle_name, i.job_title, i.tg_name)
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
                text += search_message(i.id, i.first_name, i.surname, i.middle_name, i.job_title, i.tg_name)
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
            text += search_message(i.id, i.first_name, i.surname, i.middle_name, i.job_title, i.tg_name)
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
                text += search_message(i.id, i.first_name, i.surname, i.middle_name, i.job_title, i.tg_name)
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
            text += search_message(i.id, i.first_name, i.surname, i.middle_name, i.job_title, i.tg_name)
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
                text += search_message(i.id, i.first_name, i.surname, i.middle_name, i.job_title, i.tg_name)
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
            employers = "\n".join(i['employers'])
            text += f"<b>{i['name']}:</b>\n" \
                    f"<b>Сотрудники:</b>\n" \
                    f"{employers}\n\n"
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
                        f"{employers}\n\n"
            await message.answer(text=f"<u>Вот, кто частично подходит под твой запрос:</u>\n\n{text}\n",
                                 parse_mode=types.ParseMode.HTML)
        await state.finish()


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
