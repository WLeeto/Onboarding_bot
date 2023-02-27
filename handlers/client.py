import asyncio

from aiogram import types, Dispatcher
from create_bot import dp, bot, db

from func.all_func import delete_message

from dicts.messages import message_dict
from keyboards.inline_find import search_way
from keyboards.inline_start_survey import Survey_inlines_keyboards


# @dp.message_handler(commands=['test'])
async def test(message: types.Message):
    answer = await message.answer('Бот работает. Сообщение будет удалено')
    await delete_message(answer, 3)


# @dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = Survey_inlines_keyboards()
    if db.is_tg_id_in_base(message.from_id):
        await message.answer(f"{message_dict['greetings']}")
        await message.answer_video(message_dict['greeting_video_id'])
        await asyncio.sleep(1)
        await message.answer(message_dict['for_olds_message'], reply_markup=keyboard.start_survey())
    else:
        await message.answer(message_dict["greeting_message"])
        await message.answer(message_dict["newbie_greeting"])


# @dp.message_handler(commands='find')
async def start_searching(messages: types.Message):
    await messages.answer("Вот клавиатура для поиска:", reply_markup=search_way)
    await messages.delete()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(test, commands=['test'])
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(start_searching, commands='find')