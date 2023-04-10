from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot, db

from States.states import FSM_newbie_questioning

from dicts.messages import operator_list
from func.all_func import is_breakes, is_reply_keyboard
from keyboards.all_keyboards import all_keyboards
from keyboards.inline_operator import operator_choice_kb_gen, operator_start_answering, auto_answers_kb_gen, \
    operator_add_new_question_kb_gen
from keyboards.inline_type_of_employement import type_of_employement_kb

from datetime import date


# Состояния для общение с оператором -----------------------------------------------------------------------------------
class FSM_operator_call(StatesGroup):
    start_answering = State()
    operator_choiсe = State()
    send_manual_answer = State()
    send_auto_answer = State()
    add_new_auto_question = State()
    add_new_manual_question = State()


# @dp.callback_query_handler(lambda c: c.data.startswith("call_operator"))
async def call_operator(callback_query: types.CallbackQuery):
    await bot.edit_message_text(text="Вопрос отправлен оператору",
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id)

    question_text = db.find_operator_question_by_id(callback_query.data.split(" ")[1])
    question_id = callback_query.data.split(" ")[1]
    question_from_user = callback_query.data.split(" ")[2]
    await callback_query.answer()
    await bot.send_message(chat_id=operator_list[0],
                           text=f"Вам новый вопрос от пользователя: {question_text},\n"
                                f"Ответишь на него ?",
                           reply_markup=operator_start_answering(question_id, question_from_user))


# @dp.callback_query_handler(lambda c: c.data.startswith("help_with_answer"), state=None)
async def operator_choiсe(callback_query: types.CallbackQuery, state=FSMContext):
    await callback_query.message.delete()

    await FSM_operator_call.operator_choiсe.set()
    async with state.proxy() as data:
        data['question_text'] = db.find_operator_question_by_id(callback_query.data.split(" ")[1])
        data["question_from_user"] = callback_query.data.split(" ")[2]
    await callback_query.answer()
    await callback_query.message.answer("Ответим вручную или выберем из списка ответов ?",
                                        reply_markup=operator_choice_kb_gen())


# @dp.callback_query_handler(lambda c: c.data.startswith("choice"), state=FSM_operator_call.operator_choiсe)
async def operator_answer(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()

    await callback_query.answer()
    if callback_query.data.split(" ")[1] == "manual":
        await FSM_operator_call.send_manual_answer.set()
        to_delete = await callback_query.message.answer("Введите ответ, который перешлем пользователю:")
        async with state.proxy() as data:
            data["to_delete"] = to_delete.message_id
    else:
        await FSM_operator_call.send_auto_answer.set()
        await callback_query.message.answer("Выбери из списка что ответим:\n", reply_markup=auto_answers_kb_gen())


# @dp.callback_query_handler(lambda c: c.data.startswith("auto_answer"), state=FSM_operator_call.send_auto_answer)
async def operator_send_auto_answer(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()

    if callback_query.data.split(" ")[1] == "manual":
        await FSM_operator_call.send_manual_answer.set()
        to_delete = await callback_query.message.answer("Введите ответ, который перешлем пользователю:")
        async with state.proxy() as data:
            data["to_delete"] = to_delete.message_id
    else:
        async with state.proxy() as data:
            chat_id = data["question_from_user"]
            question_text = data['question_text']
            data["answer_id"] = callback_query.data.split(" ")[1]
        answer_id = data["answer_id"]
        text = db.find_answer_by_answer_id(answer_id).answer_text
        answer_shortkey = db.find_answer_by_answer_id(answer_id).answer_discription
        check_keyboards = is_reply_keyboard(text)
        if check_keyboards:
            keyboard = all_keyboards[check_keyboards[-1]]
            await bot.send_message(chat_id=chat_id,
                                   text=f"<b>Оператор ответил на ваш вопрос:</b>\n"
                                        f"{question_text}\n\n"
                                        f"<b>Ответ оператора:</b>\n"
                                        f"{is_breakes(check_keyboards[0])}", parse_mode=types.ParseMode.HTML,
                                   reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=chat_id,
                                   text=f"<b>Оператор ответил на ваш вопрос:</b>\n"
                                        f"{question_text}\n\n"
                                        f"<b>Ответ оператора:</b>\n"
                                        f"{is_breakes(text)}", parse_mode=types.ParseMode.HTML)
        await callback_query.message.answer(f"Я отправил ответ:\n\n"
                                            f"{text}\n\n"
                                            f"Пользователю", parse_mode=types.ParseMode.HTML)
        await callback_query.message.answer(f"Привязать вопрос {question_text} к быстрому ответу {answer_shortkey} ?",
                                            reply_markup=operator_add_new_question_kb_gen())
        await FSM_operator_call.add_new_auto_question.set()


# @dp.callback_query_handler(lambda c: c.data.startswith("add_answer"),
#                            state=FSM_operator_call.add_new_auto_question)
async def add_new_auto_question(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    async with state.proxy() as data:
        question_text = data['question_text']
        answer_id = data["answer_id"]
    if callback_query.data.split(" ")[1] == "yes":
        add_question = db.add_question(question=question_text, answer_id=answer_id)
        if add_question:
            await callback_query.message.answer("Я привязал вопрос пользователя к ответу, "
                                                "в следующий раз отвечу на него сам")
    else:
        await callback_query.message.answer(F"Я отправил ответ пользователю. В БД ничего не добавлял.")
    await state.finish()


# @dp.callback_query_handler(lambda c: c.data.startswith("add_answer"),
# state=FSM_operator_call.add_new_auto_question)
async def operator_adds_new_auto_question(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.answer()
    async with state.proxy() as data:
        answer_id = data["answer_id"]
        question_text = data['question_text']
    if callback_query.data.split(" ")[1] == "yes":
        db.add_question(question=question_text, answer_id=answer_id)
        await callback_query.message.answer("Я добавил этот вопрос в БД, в следующий раз я отвечу на него сам ;)")
    else:
        await callback_query.message.answer("Я не добавлял ничего в БД")


# @dp.message_handler(state=FSM_operator_call.send_manual_answer)
async def operator_manual_answer(message: types.Message, state: FSMContext):
    await message.delete()
    answer = message.text
    async with state.proxy() as data:
        chat_id = data["question_from_user"]
        question_text = data["question_text"]
        data["manual_answer_text"] = answer
        to_delete = data["to_delete"]
    await bot.delete_message(message.from_id, to_delete)
    await bot.send_message(chat_id=chat_id,
                           text=f"<b>Оператор ответил на ваш вопрос:</b>\n"
                                f"{question_text}\n\n"
                                f"<b>Ответ оператора:</b>\n"
                                f"{answer}")
    await message.answer("Добавить вопрос пользователя и ваш ответ в БД ?\n"
                         "В этом случае в следующий раз я смогу ответить самостоятельно",
                         reply_markup=operator_add_new_question_kb_gen())
    await FSM_operator_call.add_new_manual_question.set()


# @dp.callback_query_handler(lambda c: c.data.startswith("add_answer"), state=FSM_operator_call.add_new_manual_question)
async def operator_adds_new_manual_question(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()

    await callback_query.answer()
    async with state.proxy() as data:
        question_text = data["question_text"]
        answer_text = data["manual_answer_text"]
    if callback_query.data.split(" ")[1] == "yes":

        operator_id = callback_query.message.from_id
        db.add_new_question_and_answer(question_text=question_text,
                                       answer_text=answer_text,
                                       added_by_tg_id=operator_id)
        await callback_query.message.answer(f"Я добавил вопрос:\n"
                                            f"{question_text}\n"
                                            f"С ответом:\n"
                                            f"{answer_text}\n"
                                            f"В свою БД. В следующий раз на подобный вопрос я отвечу сам")
    else:
        await callback_query.message.answer(f"Ок. Я отправил ответ {answer_text} пользователю")
    await state.finish()


# ----------------------------------------------------------------------------------------------------------------------
# @dp.callback_query_handler(lambda c: c.data.startswith("new_user"), state=FSM_newbie_questioning.accept_new_user)
async def catch_new_user(callback_query: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        confirming_user = db.find_one_confirming_user()
        data["confirming_user_id"] = confirming_user.id
        data["confirming_user_tg_name"] = confirming_user.tg_name
        data["confirming_user_tg_id"] = confirming_user.tg_id
        data["confirming_user_phone"] = confirming_user.phone
        data["confirming_user_email"] = confirming_user.email
        data["confirming_user_first_name"] = confirming_user.first_name
        data["confirming_user_surname"] = confirming_user.surname
        data["confirming_user_middle_name"] = confirming_user.middle_name
        data["confirming_user_bdate"] = confirming_user.date_of_birth
        data["confirming_user_tg_photo"] = confirming_user.tg_photo
        data["confirming_user_hobby"] = confirming_user.hobby
        db.clear_newbee_confirming(data["confirming_user_id"])
    await callback_query.answer()
    if callback_query.data.split(" ")[1] == "ok":
        await FSM_newbie_questioning.save_job_title.set()
        await callback_query.message.answer(f"Отлично, давай тогда добавим несколько данных"
                                            f" по этому сотруднику и внесем его в базу:\n"
                                            f"Введи должность нового сотрудника")
    else:
        await FSM_newbie_questioning.confirm_failed.set()
        await callback_query.message.answer("Введите комментарий для анкеты. "
                                            "Я отправлю его пользователю с просьбой заполнить анкету заново:")


# @dp.message_handler(state=FSM_newbie_questioning.confirm_failed)
async def send_comfirm_failed_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        chat_id = data["confirming_user_tg_id"]
    comment = message.text
    await bot.send_message(chat_id=chat_id, text=f"Администратор отклонил вашу анкету с комментарием:\n"
                                                 f"<b>{comment}</b>\n"
                                                 "Пожалуйста используйте /start чтобы заполнить анкету заново.",
                           parse_mode=types.ParseMode.HTML)
    await message.answer("Комментарий отправлен пользователю")
    await state.finish()


# @dp.message_handler(state=FSM_newbie_questioning.save_job_title)
async def save_job_title(message: types.Message, state: FSMContext):
    await FSM_newbie_questioning.save_type_of_employement.set()
    async with state.proxy() as data:
        data["job_title"] = message.text
    await message.answer("Какой тип трудоустройства у сотрудника ?:", reply_markup=type_of_employement_kb)


# @dp.callback_query_handler(lambda c: c.data.startswith("type_of_emp"),
#                            state=FSM_newbie_questioning.save_type_of_employement)
async def add_new_user_to_db(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback_query.data.split(" ")[1] == "state":
            data["type_of_employement"] = "штат"
        elif callback_query.data.split(" ")[1] == "ip":
            data["type_of_employement"] = "ип"
        elif callback_query.data.split(" ")[1] == "gph":
            data["type_of_employement"] = "гпх"
        elif callback_query.data.split(" ")[1] == "sz":
            data["type_of_employement"] = "сз"

    async with state.proxy() as data:
        confirming_user_tg_id = data["confirming_user_tg_id"]
        confirming_user_tg_name = data["confirming_user_tg_name"]
        confirming_user_phone = data["confirming_user_phone"]
        confirming_user_email = data["confirming_user_email"]
        confirming_user_first_name = data["confirming_user_first_name"]
        confirming_user_surname = data["confirming_user_surname"]
        confirming_user_middle_name = data["confirming_user_middle_name"]
        confirming_user_bdate = data["confirming_user_bdate"]
        confirming_user_tg_photo = data["confirming_user_tg_photo"]
        confirming_user_hobby = data["confirming_user_hobby"]

    db.add_new_user(
        tg_id=confirming_user_tg_id,
        first_name=confirming_user_first_name,
        surname=confirming_user_surname,
        job_title=data["job_title"],
        tg_name=confirming_user_tg_name,
        hired_at=date.today(),
        middle_name=confirming_user_middle_name,
        type_of_employment=data["type_of_employement"],
        date_of_birth=confirming_user_bdate,
        tg_photo=confirming_user_tg_photo,
        hobby=confirming_user_hobby,
    )

    new_user_id = db.find_by_tg_id(confirming_user_tg_id).id
    new_phone = db.add_new_contact(profile_id=new_user_id,
                                   contact_type="P",
                                   contact=confirming_user_phone
                                   )
    new_email = db.add_new_contact(
        profile_id=new_user_id,
        contact_type="@",
        contact=confirming_user_email
    )

    await state.finish()
    if new_phone and new_email:
        await callback_query.message.answer("Отлично ! Я добавил нового сотрудника в БД")
    else:
        await callback_query.message.answer("Что-то пошло не так, пользователь не был добавлен")


def register_handlers_operator(dp: Dispatcher):
    dp.register_callback_query_handler(catch_new_user,
                                       lambda c: c.data.startswith("new_user"),
                                       state=FSM_newbie_questioning.accept_new_user)
    dp.register_message_handler(send_comfirm_failed_message, state=FSM_newbie_questioning.confirm_failed)
    dp.register_message_handler(save_job_title, state=FSM_newbie_questioning.save_job_title)
    dp.register_callback_query_handler(add_new_user_to_db, lambda c: c.data.startswith("type_of_emp"),
                                       state=FSM_newbie_questioning.save_type_of_employement)

    dp.register_callback_query_handler(call_operator, lambda c: c.data.startswith("call_operator"))
    dp.register_callback_query_handler(operator_choiсe, lambda c: c.data.startswith("help_with_answer"), state=None)
    dp.register_callback_query_handler(operator_answer,
                                       lambda c: c.data.startswith("choice"),
                                       state=FSM_operator_call.operator_choiсe)
    dp.register_message_handler(operator_manual_answer, state=FSM_operator_call.send_manual_answer)
    dp.register_callback_query_handler(operator_send_auto_answer,
                                       lambda c: c.data.startswith("auto_answer"),
                                       state=FSM_operator_call.send_auto_answer)
    dp.register_callback_query_handler(operator_adds_new_auto_question,
                                       lambda c: c.data.startswith("add_answer"),
                                       state=FSM_operator_call.add_new_auto_question)
    dp.register_callback_query_handler(add_new_auto_question, lambda c: c.data.startswith("add_answer"),
                                       state=FSM_operator_call.add_new_auto_question)
    dp.register_callback_query_handler(operator_adds_new_manual_question,
                                       lambda c: c.data.startswith("add_answer"),
                                       state=FSM_operator_call.add_new_manual_question)
