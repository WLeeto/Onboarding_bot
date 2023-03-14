from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot, db

from func.all_func import is_breakes


# @dp.callback_query_handler(lambda c: c.data.startswith("project"), state=None)
async def projects(callback_querry: types.CallbackQuery):
    project = callback_querry.data.split(" ")[1]
    text = db.find_project_text_by_id(project)
    await callback_querry.answer()
    await callback_querry.message.answer(is_breakes(text), parse_mode=types.ParseMode.HTML)


def register_handlers_projects(dp: Dispatcher):
    dp.register_callback_query_handler(projects, lambda c: c.data.startswith("project"), state=None)