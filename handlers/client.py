import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from create_bot import dp, bot, db

from func.all_func import delete_message

from dicts.messages import message_dict, commands_dict
from keyboards.inline_find import search_way
from keyboards.inline_initiate_vacation import start_sending_vacation_email_button, \
    start_sending_vacation_email_keyboard, vacation_keyboard
from keyboards.inline_projects import Projects_keyboard
from keyboards.inline_start_survey import Survey_inlines_keyboards
from keyboards.inline_get_documents import get_business_trip_docs_keyboard, get_teamforce_presentation_keyboard, \
    get_annual_leave
from keyboards.inline_contacts import contacts_keyboard

from handlers.other import FSM_newbie_questioning, FSM_search, FSMContext, FSM_start_survey


# Состояния для ввода типа трудоустройства -----------------------------------------------------------------------------
class FSM_type_of_employment(StatesGroup):
    change_type_of_employment = State()


# @dp.message_handler(state=FSM_type_of_employment.change_type_of_employment)
async def change_type_of_employement(message: types.Message, state: FSMContext):
    types_list = ["штат", "сз", "ип", "гпх"]
    user_id = message.from_user.id
    type_of_employement = message.text.lower()
    if type_of_employement in types_list:
        db.change_type_of_employment(tg_id=user_id, type_of_employement=type_of_employement)
        await state.finish()
        await message.answer(f"Ваш статус трудоустройства был изменен на {type_of_employement}\n"
                             f"Теперь можно повторить команду =)")
    else:
        text = ""
        for i in types_list:
            text += f"{i}, "
        await message.answer(f"Тип занятости может быль только: {text}")


# ----------------------------------------------------------------------------------------------------------------------


# @dp.message_handler(commands='vacation')
async def vacation(message: types.Message):
    type_of_employement = db.what_type_of_employment(message.from_id)
    if type_of_employement:
        await message.answer(commands_dict["vacation"]["vacation"], parse_mode=types.ParseMode.HTML,
                             reply_markup=vacation_keyboard)
    else:
        await FSM_type_of_employment.change_type_of_employment.set()
        await message.answer("Я не нашел в своей базе тип твоей занятости в компании Тимфорс.\n"
                             "Укажи пожалуйста ты оформлен в штат или работаешь по ИП/СЗ/ГПХ ?",
                             parse_mode=types.ParseMode.HTML)


# @dp.message_handler(commands=['test'])
async def test(message: types.Message):
    answer = await message.answer(f'Ваш id: {message.from_id}\n'
                                  f'Бот работает. Сообщение будет удалено')
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


# @dp.message_handler(commands='stop', state=FSM_start_survey.all_states)
async def stop(message: types.Message, state="*"):
    db.close_session()
    await state.finish()
    answer = await message.answer("Выполнено. Сообщение будет удалено")
    await asyncio.create_task(delete_message(answer, 3))


# @dp.message_handler(commands='help')
async def help(message: types.Message):
    await message.answer(message_dict["help"])


# @dp.message_handler(commands='find')
async def start_searching(messages: types.Message):
    await messages.answer("Вот клавиатура для поиска:", reply_markup=search_way)
    await messages.delete()


# @dp.message_handler(commands='contacts')
async def contacts(message: types.Message):
    await message.answer(commands_dict["contacts"], parse_mode=types.ParseMode.HTML, reply_markup=contacts_keyboard)


# @dp.message_handler(commands='benefits')
async def benefits(message: types.Message):
    await message.answer(commands_dict["benefits"], parse_mode=types.ParseMode.HTML,
                         reply_markup=get_teamforce_presentation_keyboard)


# # @dp.message_handler(commands='docs')
# async def docs(message: types.Message):
#     await message.answer(commands_dict["docs"], parse_mode=types.ParseMode.HTML)


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


# @dp.message_handler(commands='office')
async def office(message: types.Message):
    await message.answer(commands_dict["office"], parse_mode=types.ParseMode.HTML)


# @dp.message_handler(commands='business_trip')
async def business_trip(message: types.Message):
    await message.answer(commands_dict["business_trip"], parse_mode=types.ParseMode.HTML,
                         reply_markup=get_business_trip_docs_keyboard)


# @dp.message_handler(commands='referal')
async def referal(message: types.Message):
    await message.answer(commands_dict["referal"], parse_mode=types.ParseMode.HTML)


# @dp.message_handler(commands='tf360')
async def tf360(message: types.Message):
    await message.answer(commands_dict["tf360"], parse_mode=types.ParseMode.HTML)


# @dp.message_handler(commands='projects')
async def projects(message: types.Message):
    projects_kb = Projects_keyboard()
    await message.answer(commands_dict["projects"], parse_mode=types.ParseMode.HTML,
                         reply_markup=projects_kb.create_kb())


def register_handlers_client(dp: Dispatcher):

    dp.register_message_handler(stop, commands='stop', state="*")

    dp.register_message_handler(change_type_of_employement, state=FSM_type_of_employment.change_type_of_employment)
    dp.register_message_handler(projects, commands='projects')
    dp.register_message_handler(test, commands='test')
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(help, commands='help')
    dp.register_message_handler(start_searching, commands='find')
    dp.register_message_handler(contacts, commands='contacts')
    dp.register_message_handler(vacation, commands='vacation')
    dp.register_message_handler(benefits, commands='benefits')
    # dp.register_message_handler(docs, commands='docs')
    dp.register_message_handler(support, commands='support')
    dp.register_message_handler(social_media, commands='social_media')
    dp.register_message_handler(initiative, commands='initiative')
    dp.register_message_handler(finance, commands='finance')
    dp.register_message_handler(office, commands='office')
    dp.register_message_handler(business_trip, commands='business_trip')
    dp.register_message_handler(referal, commands='referal')
    dp.register_message_handler(tf360, commands='tf360')
