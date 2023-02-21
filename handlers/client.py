from aiogram import Dispatcher
from aiogram import types, Dispatcher
from create_bot import dp, bot

from func.all_func import delete_message

from dicts.messages import message_dict
from keyboards.inline_find import search_way


# @dp.message_handler(commands=['test'])
async def test(message: types.Message):
    answer = await message.answer('Бот работает. Сообщение будет удалено')
    await delete_message(answer, 3)


# @dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    await message.answer(message_dict['greetings'])


# @dp.message_handler(commands='find')
async def start_searching(messages: types.Message):
    await messages.answer("Вот клавиатура для поиска:", reply_markup=search_way)
    await messages.delete()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(test, commands=['test'])
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(start_searching, commands='find')