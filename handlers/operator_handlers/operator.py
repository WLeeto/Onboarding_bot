from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot, db

from dicts.messages import operator_list
from keyboards.inline_operator import operator_choice_kb_gen, operator_start_answering


# Состояния для общение с оператором -----------------------------------------------------------------------------------
class FSM_operator_call(StatesGroup):
    operator_start = State()
    operator_choice = State()
    enter_answer = State()


@dp.callback_query_handler(lambda c: c.data.startswith("call_operator"), state=None)
async def call_operator(callback_query: types.CallbackQuery, state: FSMContext):
    await FSM_operator_call.operator_start.set()
    await callback_query.message.edit_text("Вопрос отправлен оператору, ожидайте ответа")
    question_id = callback_query.data.split(" ")[1]
    text = db.find_operator_question_by_id(question_id)
    await bot.send_message(chat_id=operator_list[0],
                           text=f"Новый вопрос от пользователя. Помоги пожалуйста ответить:\n"
                                f"{callback_query.from_user.id} {callback_query.from_user.username} спрашивает:\n"
                                f"{text}\n\n"
                                f"Чтобы ответить нажми на кнопку:",
                           reply_markup=operator_start_answering())


@dp.callback_query_handler(lambda c: c.data == "help_with_answer", state=None)
async def operator_start_answer(callback_query: types.CallbackQuery, state: FSMContext):
    await FSM_operator_call.operator_choice.set()
    await callback_query.message.answer("Можем ввести ответ вручную или выбрать из списка уже имеющихся:",
                                        reply_markup=operator_choice_kb_gen())


@dp.callback_query_handler(lambda c: c.data.startswith("choice"), state=FSM_operator_call.operator_choice)
async def operator_choice(callback_query: types.CallbackQuery, state=FSMContext):
    if callback_query.data.split(" ")[1] == "manual":
        await FSM_operator_call.enter_answer.set()
        await callback_query.message.answer("Введите ответ:")
    elif callback_query.data.split(" ")[1] == "from":
        pass


@dp.message_handler(state=FSM_operator_call.enter_answer)
async def answer_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await state.finish()
        await bot.send_message(chat_id=data["user_id"], text=message.text)
        await message.answer("Ответ отправлен пользователю")


def register_handlers_operator(dp: Dispatcher):
    pass
    # dp.register_callback_query_handler(call_operator, lambda c: c.data.startswith("call_operator"),
    #                                    state=FSM_operator_call.operator_start)
    # dp.register_callback_query_handler(operator_choice,
    #                                    lambda c: c.data.startswith("choice"), state=FSM_operator_call.operator_start)
    #
    # dp.register_message_handler(answer_question, state=FSM_operator_call.enter_answer)