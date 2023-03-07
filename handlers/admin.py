from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot, db

from database.requests import database

import asyncio

from func.all_func import delete_message
from fill_db_script import fill_db

admins = [5148438149, ]


# Состояния для добавления нового ответа -------------------------------------------------------------------------------
class FSM_db_add_answer(StatesGroup):
    add_new_answer = State()


# @dp.message_handler(commands='addanswer', state=None)
async def add_answer(message: types.Message):
    await FSM_db_add_answer.add_new_answer.set()
    await message.answer('Какой ответ добавим ?')


# @dp.message_handler(content_types='text', state=FSM_db_add.add_new_answer)
async def entering_new_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['answer'] = message.text
    result = db.add_answer(data['answer'])
    await message.answer(result)
    await state.finish()


# @dp.message_handler(commands='allanswers')
async def display_all_answers(message: types.Message):
    result = db.find_all_answers()
    msg = ''
    for key, value in result.items():
        msg += f'id {key} - {value}\n'
    await message.answer(msg)


# Состояния для добавления вопроса и привязки его к ответу -------------------------------------------------------------
class FSM_db_add_question(StatesGroup):
    add_new_question = State()
    bind_answer = State()


# @dp.message_handler(commands='addquestion', state=None)
async def add_question(message: types.Message):
    await FSM_db_add_question.add_new_question.set()
    await message.answer('Какой вопрос добавим ?')


# @dp.message_handler(content_types='text', state=FSM_db_add_question.add_new_question)
async def entering_new_question(message: types.Message, state: FSM_db_add_question):
    async with state.proxy() as data:
        data['question'] = message.text
    await FSM_db_add_question.next()
    await message.answer('К какому ответу привяжем (укажите id ответа)?')


# @dp.message_handler(content_types='text', state=FSM_db_add_question.bind_answer)
async def binding_answer(message: types.Message, state: FSM_db_add_question):
    async with state.proxy() as data:
        data['answer_id'] = message.text
    result = db.add_question(data['question'], data['answer_id'])
    await message.answer(result)
    await state.finish()


# @dp.message_handler(commands='allquestions')
async def display_all_questions(message: types.Message):
    result = db.find_all_questions()
    msg = ''
    for value in result.values():
        msg += f'{value}\n'
    await message.answer(msg)


# @dp.message_handler(commands='_resetdb')
async def reset_db(message: types.Message):
    if message.from_user.id in admins:
        db.drop_tables()
        db.create_tables()
        await message.answer('БД была сброшена. Если вы ввели команду случайно, то все плохо.')
    else:
        await message.answer('Эта команда только для администраторов')


# @dp.message_handler(commands='_filldb')
async def filldb(message: types.Message):
    if message.from_user.id in admins:
        fill_db()
        await message.answer("База данных заполнена тестовыми данными")
    else:
        await message.answer("Эта команда толко для администраторов")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(add_answer, commands='addanswer', state=None)
    dp.register_message_handler(entering_new_answer, content_types='text', state=FSM_db_add_answer.add_new_answer)
    dp.register_message_handler(display_all_answers, commands='allanswers')
    dp.register_message_handler(add_question, commands='addquestion')
    dp.register_message_handler(entering_new_question, content_types='text', state=FSM_db_add_question.add_new_question)
    dp.register_message_handler(binding_answer, content_types='text', state=FSM_db_add_question.bind_answer)
    dp.register_message_handler(display_all_questions, commands='allquestions')
    dp.register_message_handler(reset_db, commands='_resetdb')
    dp.register_message_handler(filldb, commands='_filldb')