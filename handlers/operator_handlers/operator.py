from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot, db

from dicts.messages import operator_list
from func.all_func import is_breakes
from keyboards.inline_operator import operator_choice_kb_gen, operator_start_answering, auto_answers_kb_gen, \
    operator_add_new_question_kb_gen


# Состояния для общение с оператором -----------------------------------------------------------------------------------
class FSM_operator_call(StatesGroup):
    start_answering = State()
    operator_choiсe = State()
    send_manual_answer = State()
    send_auto_answer = State()
    add_new_auto_question = State()
    add_new_manual_question = State()


# @dp.callback_query_handler(lambda c: c.data.startswith("call_operator"))
async def call_operator(callback_querry: types.CallbackQuery, state: FSMContext):
    question_text = db.find_operator_question_by_id(callback_querry.data.split(" ")[1])
    question_id = callback_querry.data.split(" ")[1]
    question_from_user = callback_querry.data.split(" ")[2]
    await callback_querry.answer()
    await bot.send_message(chat_id=operator_list[0],
                           text=f"Вам новый вопрос от пользователя: {question_text},\n"
                                f"Ответишь на него ?",
                           reply_markup=operator_start_answering(question_id, question_from_user))


# @dp.callback_query_handler(lambda c: c.data.startswith("help_with_answer"), state=None)
async def operator_choiсe(callback_query: types.CallbackQuery, state=FSMContext):
    await FSM_operator_call.operator_choiсe.set()
    async with state.proxy() as data:
        data['question_text'] = db.find_operator_question_by_id(callback_query.data.split(" ")[1])
        data["question_from_user"] = callback_query.data.split(" ")[2]
    await callback_query.answer()
    await callback_query.message.answer("Ответим вручную или выберем из списка ответов ?",
                                        reply_markup=operator_choice_kb_gen())


# @dp.callback_query_handler(lambda c: c.data.startswith("choice"), state=FSM_operator_call.operator_choiсe)
async def operator_answer(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    if callback_query.data.split(" ")[1] == "manual":
        await FSM_operator_call.send_manual_answer.set()
        await callback_query.message.answer("Введите ответ, который перешлем пользователю:")
    else:
        await FSM_operator_call.send_auto_answer.set()
        await callback_query.message.answer("Выбери из списка что ответим:\n", reply_markup=auto_answers_kb_gen())


# @dp.callback_query_handler(lambda c: c.data.startswith("auto_answer"), state=FSM_operator_call.send_auto_answer)
async def operator_send_auto_answer(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data.split(" ")[1] == "manual":
        await FSM_operator_call.send_manual_answer.set()
        await callback_query.message.answer("Введите ответ, который перешлем пользователю:")
        return
    async with state.proxy() as data:
        chat_id = data["question_from_user"]
        question_text = data['question_text']
        data["answer_id"] = callback_query.data.split(" ")[1]
    answer_id = data["answer_id"]
    text = db.find_answer_by_answer_id(answer_id).answer_text
    await bot.send_message(chat_id=chat_id,
                           text=f"Оператор ответил на ваш вопрос:\n"
                                f"{question_text}\n\n"
                                f"Ответ оператора:\n"
                                f"{is_breakes(text)}")
    await FSM_operator_call.add_new_auto_question.set()
    await callback_query.message.answer("Добавить вопрос пользователя в БД ?",
                                        reply_markup=operator_add_new_question_kb_gen())


# @dp.callback_query_handler(lambda c: c.data.startswith("add_answer"),
# state=FSM_operator_call.add_new_auto_question)
async def operator_adds_new_auto_question(callback_query: types.CallbackQuery, state: FSMContext):
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
    answer = message.text
    async with state.proxy() as data:
        chat_id = data["question_from_user"]
        question_text = data['question_text']
        data["manual_answer_text"] = answer
    await bot.send_message(chat_id=chat_id,
                           text=f"Оператор ответил на ваш вопрос:\n"
                                f"{question_text}\n\n"
                                f"Ответ оператора:\n"
                                f"{answer}")
    await message.answer("Добавить вопрос пользователя и ваш ответ в БД ?\n"
                         "В этом случае в следующий раз я смогу ответить самостоятельно",
                         reply_markup=operator_add_new_question_kb_gen())
    await FSM_operator_call.add_new_manual_question.set()


# @dp.callback_query_handler(lambda c: c.data.startswith("add_answer"), state=FSM_operator_call.add_new_manual_question)
async def operator_adds_new_manual_question(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    if callback_query.data.split(" ")[1]:
        async with state.proxy() as data:
            question_text = data["question_text"]
            answer_text = data["manual_answer_text"]
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
        await callback_query.message.answer("Ок =)")
    await state.finish()


def register_handlers_operator(dp: Dispatcher):
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
    dp.register_callback_query_handler(operator_adds_new_manual_question,
                                       lambda c: c.data.startswith("add_answer"),
                                       state=FSM_operator_call.add_new_manual_question)
