from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot, db

from dicts.messages import operator_list


# Состояния для общение с оператором -----------------------------------------------------------------------------------
# @dp.callback_query_handler(lambda c: c.data.startswith("call_operator"), state=None)
async def call_operator(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Вопрос отправлен оператору, ожидайте ответа")
    question_id = callback_query.data.split(" ")[1]
    text = db.find_operator_question_by_id(question_id)
    await bot.send_message(chat_id=operator_list[0],
                           text=f"Новый вопрос от пользователя. Помоги пожалуйста ответить:\n"
                                f"{callback_query.from_user.id} {callback_query.from_user.username} спрашивает:\n"
                                f"{text}")


def register_handlers_operator(dp: Dispatcher):
    dp.register_callback_query_handler(call_operator, lambda c: c.data.startswith("call_operator"), state=None)