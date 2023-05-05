import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import WrongFileIdentifier

from create_bot import dp, bot, db

from func.all_func import delete_message, is_breakes, is_reply_keyboard

from dicts.messages import message_dict, commands_dict, operator_list, administarator_list
from keyboards.all_keyboards import all_keyboards
from keyboards.inline_bday import bday_kb
from keyboards.inline_create_kb import create_kb
from keyboards.inline_find import search_way
from keyboards.inline_initiate_vacation import vacation_keyboard
from keyboards.inline_projects import Projects_keyboard
from keyboards.inline_sick_leave import sick_leave_kb
from keyboards.inline_start_survey import Survey_inlines_keyboards
from keyboards.inline_get_documents import get_business_trip_docs_keyboard, get_teamforce_presentation_keyboard
from keyboards.inline_contacts import contacts_keyboard
from keyboards.inline_type_of_employement import type_of_employement_kb

from handlers.other import FSMContext

from States.states import FSM_type_of_employment, FSM_meeting, FSM_newbie_questioning
from keyboards.inline_xlsx_newbie_form import start_kb


# @dp.callback_query_handler(lambda c: c.data.startswith("type_of_emp"),
#                            state=FSM_type_of_employment.change_type_of_employment)
async def change_type_of_employement(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    type_of_employement = None
    if callback_query.data.split(" ")[1] == "state":
        type_of_employement = "штат"
    elif callback_query.data.split(" ")[1] == "ip":
        type_of_employement = "ип"
    elif callback_query.data.split(" ")[1] == "gph":
        type_of_employement = "гпх"
    elif callback_query.data.split(" ")[1] == "sz":
        type_of_employement = "сз"
    db.change_type_of_employment(tg_id=user_id, type_of_employement=type_of_employement)
    await state.finish()
    await callback_query.message.answer(
        f"Ваш статус трудоустройства был изменен на <u>'{type_of_employement.capitalize()}'</u>\n"
        f"Теперь можно повторить команду =)",
        parse_mode=types.ParseMode.HTML
    )


# ----------------------------------------------------------------------------------------------------------------------


# @dp.message_handler(commands='vacation')
async def vacation(message: types.Message):
    user = db.is_user(message.from_id)
    if user:
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="vacation")
        type_of_employement = db.what_type_of_employment(message.from_id)
        if type_of_employement:
            await message.answer(commands_dict["vacation"]["vacation"], parse_mode=types.ParseMode.HTML,
                                 reply_markup=vacation_keyboard)
        else:
            await FSM_type_of_employment.change_type_of_employment.set()
            await message.answer("Я не нашел в своей базе тип твоей занятости в компании ТИМ ФОРС.\n"
                                 "Укажи, пожалуйста, ты оформлен в штат или работаешь по ИП/СЗ/ГПХ ?",
                                 reply_markup=type_of_employement_kb,
                                 parse_mode=types.ParseMode.HTML)
    else:
        await message.answer("Я не смог найти вас в БД. Вы у нас работаете ?")


# @dp.message_handler(commands=['test'])
async def test(message: types.Message):
    answer = await message.answer(f'Ваш id: `{message.from_id}`\n'
                                  f'Бот работает. Сообщение будет удалено', parse_mode=types.ParseMode.MARKDOWN)
    await asyncio.create_task(delete_message(answer, 3))


# @dp.message_handler(commands=['start'])
async def start(message: types.Message, state=FSMContext):
    db.close_session()
    await state.finish()
    if not db.find_statistics(message.from_id):
        db.add_statistics(message.from_id)
    keyboard = Survey_inlines_keyboards()
    me = await bot.get_me()
    user = db.is_user(message.from_id)
    if user:
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="start")
        await message.answer(message_dict['greetings'], parse_mode=types.ParseMode.HTML)
        try:
            await message.answer_video(message_dict["greeting_video_id"])
        except WrongFileIdentifier as ex:
            print(f"Не удалось загрузить видео:\n"
                  f"{ex}")
        await asyncio.sleep(3)
        await message.answer(message_dict['for_olds_message'], reply_markup=keyboard.start_survey())
    elif db.is_tg_id_in_newbie_base(message.from_id):
        await FSM_newbie_questioning.newbie_questioning_start.set()
        await message.answer(message_dict["greetings"])
        await message.answer(message_dict["newbie_greeting"].format(bot_name=f"@{me.username}"),
                             reply_markup=keyboard.ok_keyboard())
    else:
        await message.answer(message_dict["start_not_in_db"].format(tgid=message.from_id),
                             parse_mode=types.ParseMode.MARKDOWN_V2, disable_web_page_preview=True)


# @dp.message_handler(commands='stop', state=FSM_start_survey.all_states)
async def stop(message: types.Message, state=FSMContext):
    db.close_session()
    await state.finish()
    answer = await message.answer("Выполнено. Сообщение будет удалено")
    await asyncio.create_task(delete_message(answer, 3))


# @dp.message_handler(commands='help')
async def help(message: types.Message):
    user = db.is_user(message.from_id)
    if user:
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="help")
        await message.answer(message_dict["help_message"])
    else:
        await message.answer(message_dict["start_not_in_db"].format(tgid=message.from_id),
                             parse_mode=types.ParseMode.MARKDOWN_V2, disable_web_page_preview=True)


# @dp.message_handler(commands='find')
async def start_searching(message: types.Message):
    user = db.is_user(message.from_id)
    if user:
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="find")
        await message.answer("Клавиатура для поиска:", reply_markup=search_way)
        await message.delete()
    else:
        await message.answer(message_dict["not_in_db"])


# @dp.message_handler(commands='contacts')
async def contacts(message: types.Message):
    user = db.is_user(message.from_id)
    if user:
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="contacts")
        await message.answer(commands_dict["contacts"], parse_mode=types.ParseMode.HTML, reply_markup=contacts_keyboard)
    else:
        await message.answer(message_dict["not_in_db"])


# @dp.message_handler(commands='benefits')
async def benefits(message: types.Message):
    user = db.is_user(message.from_id)
    if user:
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="benefits")
        text = db.find_answer_by_answer_id(17).answer_text
        check_keyboards = is_reply_keyboard(text)
        if check_keyboards:
            keyboard = all_keyboards[check_keyboards[-1]]
            await message.answer(is_breakes(check_keyboards[0]), parse_mode=types.ParseMode.HTML,
                                 reply_markup=keyboard)
        else:
            await message.answer(is_breakes(text), parse_mode=types.ParseMode.HTML,
                                 reply_markup=get_teamforce_presentation_keyboard)
    else:
        await message.answer(message_dict["not_in_db"])


# @dp.message_handler(commands='support')
async def support(message: types.Message):
    user = db.is_user(message.from_id)
    if user:
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="support")
        text = db.find_answer_by_answer_id(18).answer_text
        await message.answer(is_breakes(text), parse_mode=types.ParseMode.HTML)
    else:
        await message.answer(message_dict["not_in_db"])


# @dp.message_handler(commands='social_media')
async def social_media(message: types.Message):
    user = db.is_user(message.from_id)
    if user:
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="social_media")
        text = db.find_answer_by_answer_id(19).answer_text
        await message.answer(is_breakes(text), parse_mode=types.ParseMode.HTML)
    else:
        await message.answer(message_dict["not_in_db"])


# @dp.message_handler(commands='initiative')
async def initiative(message: types.Message):
    user = db.is_user(message.from_id)
    if user:
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="initiative")
        text = db.find_answer_by_answer_id(20).answer_text
        await message.answer(text, parse_mode=types.ParseMode.HTML)
    else:
        await message.answer(message_dict["not_in_db"])


# @dp.message_handler(commands='finance')
async def finance(message: types.Message):
    user = db.is_user(message.from_id)
    if user:
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="finance")
        type_of_employment = db.what_type_of_employment(message.from_id)
        if type_of_employment:
            if type_of_employment == "штат":
                text = db.find_answer_by_answer_id(28).answer_text
                await message.answer(is_breakes(text), parse_mode=types.ParseMode.HTML)
            else:
                text = db.find_answer_by_answer_id(29).answer_text
                await message.answer(is_breakes(text), parse_mode=types.ParseMode.HTML)
        else:
            await FSM_type_of_employment.change_type_of_employment.set()
            await message.answer("Почему то у вас не указан тип трудоустройства, давайте это исправим.\n"
                                 "Как вы оформлены в компании ?", reply_markup=type_of_employement_kb)
    else:
        await message.answer(message_dict["not_in_db"])


# @dp.message_handler(commands='office')
async def office(message: types.Message):
    user = db.is_user(message.from_id)
    if user:
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="office")
        text = db.find_answer_by_answer_id(22).answer_text
        try:
            await bot.send_video(message.from_id,
                                 "BAACAgIAAxkBAAIWJGQ4EyUsVfCZSH3duWwuhsWwkKasAAKALQACZlDBSTHmsaJRH0WYLwQ")
        except WrongFileIdentifier:
            pass
        await message.answer(is_breakes(text), parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
    else:
        await message.answer(message_dict["not_in_db"])


# @dp.message_handler(commands='bt')
async def business_trip(message: types.Message):
    user = db.is_user(message.from_id)
    if user:
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="bt")
        await message.answer(commands_dict["bt"], parse_mode=types.ParseMode.HTML,
                             reply_markup=get_business_trip_docs_keyboard)
    else:
        await message.answer(message_dict["not_in_db"])


# @dp.message_handler(commands='referal')
async def referal(message: types.Message):
    user = db.is_user(message.from_id)
    if user:
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="referal")
        text = db.find_answer_by_answer_id(26).answer_text
        await message.answer(is_breakes(text), parse_mode=types.ParseMode.HTML)
    else:
        await message.answer(message_dict["not_in_db"])


# @dp.message_handler(commands='tf360')
async def tf360(message: types.Message):
    user = db.is_user(message.from_id)
    if user:
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="tf360")
        text = db.find_answer_by_answer_id(25).answer_text
        await message.answer(is_breakes(text), parse_mode=types.ParseMode.HTML)
    else:
        await message.answer(message_dict["not_in_db"])


# @dp.message_handler(commands='projects')
async def projects(message: types.Message):
    user = db.is_user(message.from_id)
    if user:
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="projects")
        projects_kb = Projects_keyboard()
        await message.answer(commands_dict["projects"], parse_mode=types.ParseMode.HTML,
                         reply_markup=projects_kb.create_kb())
    else:
        await message.answer(message_dict["not_in_db"])


# @dp.message_handler(commands='about')
async def about(message: types.Message):
    user = db.is_user(message.from_id)
    if user:
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="about")
        about_text = db.find_answer_by_answer_id(27).answer_text
        await message.answer(is_breakes(about_text), parse_mode=types.ParseMode.HTML)
    else:
        await message.answer(message_dict["not_in_db"])


# @dp.message_handler(commands='sick_leave')
async def sick_leave(message: types.Message):
    user = db.is_user(message.from_id)
    if user:
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="sick_leave")
        await message.answer("Что конкретно про больничный вы хотели бы узнать?:", reply_markup=sick_leave_kb)
    else:
        await message.answer(message_dict["not_in_db"])


# @dp.message_handler(commands='bday')
async def bday(message: types.Message):
    user = db.is_user(message.from_id)
    if user:
        # todo добавить проверку на тип трудоустройства
        await message.answer("Давайте посмотрим кто когда родился. Какой месяц вас интересует ?",
                             reply_markup=bday_kb)
    else:
        await message.answer(message_dict["not_in_db"])


# Добавление новенького ------------------------------------------------------------------------------------------------
class FSM_newbie_adding(StatesGroup):
    add_tg_id = State()


# @dp.message_handler(commands='adduser')
async def adduser(message: types.Message):
    if message.from_id in operator_list:
        user = db.is_user(message.from_id)
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="adduser")
        await FSM_newbie_adding.add_tg_id.set()
        await message.answer("Ура! У нас новенький ! Введи id в телеграмме чтобы добавить в БД новеньких:")
    else:
        await message.answer("Эта команда только для операторов")


# @dp.message_handler(state=FSM_newbie_adding.add_tg_id)
async def add_newbie_tg_id(message: types.Message, state: FSMContext):
    try:
        newbie_tg_id = int(message.text)
        result = db.add_newbie(newbie_tg_id=newbie_tg_id, added_by_tg_id=message.from_id)
        if result:
            await state.finish()
            await message.answer(f"Пользователь с id {newbie_tg_id} добавлен в БД пользователей\n"
                                 f"Теперь он может начать со мной разговор чтобы пройти регистрацию")
        else:
            await state.finish()
            await message.answer(f"Пользователь с id {newbie_tg_id} уже существует в БД новеньких\n"
                                 f"Он может начать со мной разговор чтобы пройти регистрацию")
    except ValueError:
        await message.answer(f"'{message.text}' не является целым числом,\n"
                             f"telegram_id могут быть только целые числа\n"
                             f"Напишите корректное telegramm id или используйте /stop для выхода")


# @dp.message_handler(commands='meeting')
async def meeting(message: types.Message):
    user = db.is_user(message.from_id)
    if user:
        db.add_statistics(tg_id=message.from_id, user_id=user.id, command_used="meeting")
        await message.answer("Давай соберем людей на созвон !\n"
                             "Напишите описание встречи и ссылку (если требуется)\n\n"
                             "Чтобы отменить создание встречи используйте /stop", parse_mode=types.ParseMode.HTML)
        await FSM_meeting.start.set()
    else:
        await message.answer(message_dict["not_in_db"])


# @dp.message_handler(commands="stat")
async def statistics(message: types.Message):
    if message.from_id in administarator_list:
        stat = db.get_full_statistics()
        start_stat = db.get_start_statistics()
        start = len(start_stat)
        command_used = 0
        contacts = 0
        vacation = 0
        benefits = 0
        support = 0
        social_media = 0
        initiative = 0
        finance = 0
        bt = 0
        find = 0
        referal = 0
        office = 0
        tf360 = 0
        projects = 0
        about = 0
        sick_leave = 0
        count = 0
        answered = 0
        not_answered = 0
        meeting = 0
        for i in stat:
            if i.command_used:
                command_used += 1
            if i.command_used == "contacts":
                contacts += 1
            if i.command_used == "vacation":
                vacation += 1
            if i.command_used == "benefits":
                benefits += 1
            if i.command_used == "support":
                support += 1
            if i.command_used == "social_media":
                social_media += 1
            if i.command_used == "initiative":
                initiative += 1
            if i.command_used == "finance":
                finance += 1
            if i.command_used == "bt":
                bt += 1
            if i.command_used == "find":
                find += 1
            if i.command_used == "referal":
                referal += 1
            if i.command_used == "office":
                office += 1
            if i.command_used == "tf360":
                tf360 += 1
            if i.command_used == "projects":
                projects += 1
            if i.command_used == "about":
                about += 1
            if i.command_used == "sick_leave":
                sick_leave += 1
            if i.command_used == "meeting":
                meeting += 1
            if i.text_request:
                count += 1
            if i.is_answered:
                answered += 1
        text = "<b><u>Статистика:</u></b>\n\n" \
               f"Всего начали работу с ботом {start} человек\n\n" \
               f"<b>Использовано команд {command_used}:</b>\n" \
               f"contacts - {contacts}\n" \
               f"vacation - {vacation}\n" \
               f"benefits - {benefits}\n" \
               f"support - {support}\n" \
               f"social_media - {social_media}\n" \
               f"initiative - {initiative}\n" \
               f"finance - {finance}\n" \
               f"bt - {bt}\n" \
               f"find - {find}\n" \
               f"referal - {referal}\n" \
               f"office - {office}\n" \
               f"tf360 - {tf360}\n" \
               f"projects - {projects}\n" \
               f"about - {about}\n" \
               f"sick_leave - {sick_leave}\n" \
               f"meeting - {meeting}" \
               f"\n" \
               f"<b>Запросов боту:</b>\n" \
               f"Всего: {count}\n" \
               f"Бот смог ответить на {answered}\n"
        await message.answer(text, parse_mode=types.ParseMode.HTML)
    else:
        await message.answer("Команда только для администраторов")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(stop, commands='stop', state="*")

    dp.register_message_handler(statistics, commands="stat")

    dp.register_message_handler(adduser, commands='adduser')
    dp.register_message_handler(add_newbie_tg_id, state=FSM_newbie_adding.add_tg_id)

    dp.register_callback_query_handler(change_type_of_employement,
                                       lambda c: c.data.startswith("type_of_emp"),
                                       state=FSM_type_of_employment.change_type_of_employment
                                       )
    dp.register_message_handler(bday, commands='bday')
    dp.register_message_handler(meeting, commands='meeting')
    dp.register_message_handler(projects, commands='projects')
    dp.register_message_handler(about, commands='about')
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
    dp.register_message_handler(business_trip, commands='bt')
    dp.register_message_handler(referal, commands='referal')
    dp.register_message_handler(tf360, commands='tf360')
    dp.register_message_handler(sick_leave, commands='sick_leave')
