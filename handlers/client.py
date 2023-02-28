import asyncio

from aiogram import types, Dispatcher
from create_bot import dp, bot, db

from func.all_func import delete_message

from dicts.messages import message_dict, commands_dict
from keyboards.inline_find import search_way
from keyboards.inline_start_survey import Survey_inlines_keyboards

from handlers.other import FSM_newbie_questioning


# @dp.message_handler(commands=['test'])
async def test(message: types.Message):
    answer = await message.answer('Бот работает. Сообщение будет удалено')
    await delete_message(answer, 3)


# @dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = Survey_inlines_keyboards()
    me = await bot.get_me()
    if db.is_tg_id_in_base(message.from_id):
        await message.answer(f"{message_dict['greetings']}")
        await message.answer_video(message_dict["greeting_video_id"])
        await asyncio.sleep(3)
        await message.answer(message_dict['for_olds_message'], reply_markup=keyboard.start_survey())
    else:
        await FSM_newbie_questioning.newbie_questioning_start.set()
        await message.answer(message_dict["greetings"])
        await message.answer(message_dict["newbie_greeting"].format(bot_name=f"@{me.username}"),
                             reply_markup=keyboard.ok_keyboard())


# @dp.message_handler(commands='help')
async def help(message: types.Message):
    await message.answer(message_dict["help"])


# @dp.message_handler(commands='find')
async def start_searching(messages: types.Message):
    await messages.answer("Вот клавиатура для поиска:", reply_markup=search_way)
    await messages.delete()


# @dp.message_handler(commands='contacts')
async def contacts(message: types.Message):
    await message.answer(commands_dict["contacts"], parse_mode=types.ParseMode.HTML)


# @dp.message_handler(commands='vacation')
async def vacation(message: types.Message):
    await message.answer(commands_dict["vacation"], parse_mode=types.ParseMode.HTML)


# @dp.message_handler(commands='benefits')
async def benefits(message: types.Message):
    await message.answer(commands_dict["benefits"], parse_mode=types.ParseMode.HTML)


# @dp.message_handler(commands='docs')
async def docs(message: types.Message):
    await message.answer(commands_dict["docs"], parse_mode=types.ParseMode.HTML)


# @dp.message_handler(commands='support')
async def support(message: types.Message):
    await message.answer(commands_dict["support"], parse_mode=types.ParseMode.HTML)


# @dp.message_handler(commands='social_media')
async def social_media(message: types.Message):
    await message.answer(commands_dict["social_media"], parse_mode=types.ParseMode.HTML)


# @dp.message_handler(commands='initiative')
async def initiative(message: types.Message):
    await message.answer(commands_dict["initiative"], parse_mode=types.ParseMode.HTML)


# @dp.message_handler(commands='finance')
async def finance(message: types.Message):
    await message.answer(commands_dict["finance"], parse_mode=types.ParseMode.HTML)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(test, commands='test')
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(help, commands='help')
    dp.register_message_handler(start_searching, commands='find')
    dp.register_message_handler(contacts, commands='contacts')
    dp.register_message_handler(vacation, commands='vacation')
    dp.register_message_handler(benefits, commands='benefits')
    dp.register_message_handler(docs, commands='docs')
    dp.register_message_handler(support, commands='support')
    dp.register_message_handler(social_media, commands='social_media')
    dp.register_message_handler(initiative, commands='initiative')
    dp.register_message_handler(finance, commands='finance')