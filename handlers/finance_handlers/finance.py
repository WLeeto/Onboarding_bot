from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot, db
from func.all_func import is_breakes


# @dp.callback_query_handler(lambda c: c.data.startswith("finance"))
async def finance_responce(callback_query: types.CallbackQuery):
    if callback_query.data.split(" ")[1] == "staff":
        text = db.find_answer_by_answer_id(28)
    else:
        text = db.find_answer_by_answer_id(29)
    await callback_query.answer()
    if text:
        await callback_query.message.edit_text(is_breakes(text.answer_text))
    else:
        await callback_query.message.edit_text("Нет ответа, проверьте id ответов в БД")


def register_handlers_finance(dp: Dispatcher):
    dp.register_callback_query_handler(finance_responce, lambda c: c.data.startswith("finance"))