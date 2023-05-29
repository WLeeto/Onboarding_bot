import asyncio
from pprint import pprint

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType

from create_bot import bot, db, dp
from dicts.messages import start_survey_dict, message_dict, commands_dict
from func.all_func import recognize_question, start_survey_answers, is_breakes, \
    is_reply_keyboard

from handlers.meeting_handlers import meeting
from handlers.newbie_questioning_handlers import newbie_questioning
from handlers.vacation_handlers import vacation
from handlers.projects_handlers import projects
from handlers.operator_handlers import operator
from handlers.finance_handlers import finance
from handlers.business_trip_handlers import business_trip
from handlers.sick_leave_handlers import sick_leave
from handlers.find_handlers import find
from handlers.create_newbie_xlsx_handlers import create_xlsx
from handlers.bday_handlers import bday

from keyboards.inline_operator import ask_operator

from keyboards.inline_start_survey import Survey_inlines_keyboards
from keyboards.all_keyboards import all_keyboards


# @dp.message_handler(content_types='text', state=None)
async def recognizing(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        user = db.is_user(message.from_id)
        if user:
            question_list = db.find_all_questions()
            response_id = recognize_question(message.text, question_list)
            if response_id:
                answered = True
                answer = db.find_answer_by_question_id(response_id)
                check_keyboards = is_reply_keyboard(answer)
                if check_keyboards:
                    keyboard = all_keyboards[check_keyboards[-1]]
                    await message.reply(is_breakes(check_keyboards[0]), reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                else:
                    await message.reply(is_breakes(answer), parse_mode=types.ParseMode.HTML)
            else:
                answered = False
                question = db.add_new_operator_question(question_text=message.text,
                                                        sender_tg_id=message.from_id,
                                                        message_id=message.message_id)
                question_id = question.id
                question_from_user = question.from_user_id
                question_message_id = question.message_id
                await message.reply("На такой запрос у меня нет ответа. Передать вопрос оператору ?",
                                    reply_markup=ask_operator(question_id, question_from_user, question_message_id))
            db.add_statistics(tg_id=message.from_user.id, user_id=user.id, text_request=message.text, is_answered=answered)
        else:
            await message.answer(message_dict["not_in_db"])


# @dp.callback_query_handler(lambda c: c.data.startswith("get"), state=None)
async def get_document(callback_query: types.CallbackQuery):
    """
    Тут парсятся все запросы документов
    """
    if callback_query.data.split(" ")[1] == "annual_leave_application":
        file_path = "documents/1_application for annual leave.doc"
    elif callback_query.data.split(" ")[1] == "business_trip_regulation":
        file_path = "documents/2 regulations on official business trips.pdf"
    elif callback_query.data.split(" ")[1] == "official_memo":
        file_path = "documents/3 official memo.docx"
    elif callback_query.data.split(" ")[1] == "application_for_funds":
        file_path = "documents/4 application for funds.doc"
    elif callback_query.data.split(" ")[1] == "teamforce_presentation":
        file_path = "documents/5 teamforce presentation.pdf"
    elif callback_query.data.split(" ")[1] == "vacation_at_own":
        file_path = "documents/6 vacation_at_own.doc"
    else:
        file_path = None

    if file_path:
        with open(file_path, "rb") as file:
            await bot.send_document(chat_id=callback_query.from_user.id, document=file)
            await callback_query.answer()


# @dp.callback_query_handler(lambda c: c.data.startswith("contacts"), state=None)
async def get_contacts(callback_query: types.CallbackQuery):
    contact_type = callback_query.data.split(" ")[1]
    if contact_type == "hr":
        await callback_query.message.edit_text(commands_dict["contacts_hr"], parse_mode=types.ParseMode.HTML)
    elif contact_type == "contracts":
        await callback_query.message.edit_text(commands_dict["contacts_contracts"], parse_mode=types.ParseMode.HTML)
    elif contact_type == "resourses":
        await callback_query.message.edit_text(commands_dict["contacts_resourses"], parse_mode=types.ParseMode.HTML)


# @dp.message_handler(content_types='video')
async def got_video(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        await message.answer(f"Получил видео. Его id {message.video.file_id}")


# @dp.message_handler(content_types=ContentType.PHOTO)
async def got_photo(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        await message.answer(message.photo[-1].file_id)


# Состояния для опросника при старте работы ----------------------------------------------------------------------------
# todo декомпозировать опросник в отдельный пакет
# todo вынести класс состояний опросника в States
class FSM_start_survey(StatesGroup):
    first_question = State()
    second_question = State()
    third_question = State()
    compare_answers = State()


# @dp.callback_query_handler(lambda c: c.data == "start_survey", state=None)
async def first_question(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data.split(" ")[1] == "yes":
        keyboard = Survey_inlines_keyboards()
        await callback_query.answer()
        await FSM_start_survey.second_question.set()
        await bot.edit_message_text(f'Первый вопрос:\n{start_survey_dict["first_question_text"]}',
                                    chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=keyboard.first_question())
    else:
        await callback_query.answer()
        await bot.edit_message_text(start_survey_dict["wana_start_no_message"],
                                    chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id, )
        await state.finish()
        await asyncio.sleep(3)
        await callback_query.message.answer(message_dict.get("help_message"))


# @dp.callback_query_handler(
#     lambda c: c.data.startswith("first"),
#     state=FSM_start_survey.second_question
# )
async def second_question(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard = Survey_inlines_keyboards()
    async with state.proxy() as answers:
        answers['first'] = callback_query.data.split(" ")[1]
    await bot.edit_message_text(f'Второй вопрос:\n{start_survey_dict["second_question_text"]}',
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=keyboard.second_question())
    await callback_query.answer()
    await FSM_start_survey.third_question.set()


# @dp.callback_query_handler(
#     lambda c: c.data.startswith("second"),
#     state=FSM_start_survey.third_question
# )
async def third_question(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard = Survey_inlines_keyboards()
    async with state.proxy() as answers:
        answers['second'] = callback_query.data.split(" ")[1]
    await bot.edit_message_text(f'Третий вопрос:\n{start_survey_dict["third_question_text"]}',
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=keyboard.third_question())
    await callback_query.answer()
    await FSM_start_survey.compare_answers.set()


# @dp.callback_query_handler(
#     lambda c: c.data.startswith("third"),
#     state=FSM_start_survey.compare_answers
# )
async def answers(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as answers:
        answers['third'] = callback_query.data.split(" ")[1]
        all_answers = start_survey_answers(answer_1=answers['first'],
                                           answer_2=answers['second'],
                                           answer_3=answers['third'])

    await bot.edit_message_text(f"<u>Сверим ответы. Внимание на экран:</u>\n\n"
                                f"{all_answers}",
                                chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                parse_mode="html"
                                )
    await callback_query.answer()
    await state.finish()
    await asyncio.sleep(3)
    await callback_query.message.answer(message_dict["we_are_closer_now"])
    await asyncio.sleep(3)
    text = db.find_answer_by_answer_id(31).answer_text
    await callback_query.message.answer(is_breakes(text), parse_mode=types.ParseMode.HTML)


# @dp.callback_query_handler(lambda c: c.data == "hr_contacts")
async def hr_contacts(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer(commands_dict["contacts_hr"], parse_mode=types.ParseMode.HTML)


def register_handlers_other(dp: Dispatcher):
    bday.register_handlers_bday(dp)
    newbie_questioning.register_handlers_newbie_questioning(dp)
    meeting.register_handlers_meeting(dp)
    sick_leave.register_handlers_sick_leave(dp)
    vacation.register_handlers_vacation(dp)
    projects.register_handlers_projects(dp)
    operator.register_handlers_operator(dp)
    finance.register_handlers_finance(dp)
    business_trip.register_handlers_business_trip(dp)
    find.register_handlers_find(dp)
    create_xlsx.register_handlers_create_xlsx(dp)

    dp.register_callback_query_handler(hr_contacts, lambda c: c.data == "hr_contacts")

    dp.register_message_handler(recognizing, content_types='text', state=None)

    dp.register_callback_query_handler(get_contacts, lambda c: c.data.startswith("contacts"), state=None)

    dp.register_callback_query_handler(get_document, lambda c: c.data.startswith("get"), state=None)

    dp.register_message_handler(got_video, content_types='video')
    dp.register_message_handler(got_photo, content_types=ContentType.PHOTO)

    dp.register_callback_query_handler(first_question, lambda c: c.data.startswith("survey"), state=None)
    dp.register_callback_query_handler(second_question, lambda c: c.data.startswith("first"),
                                       state=FSM_start_survey.second_question)
    dp.register_callback_query_handler(third_question, lambda c: c.data.startswith("second"),
                                       state=FSM_start_survey.third_question)
    dp.register_callback_query_handler(answers, lambda c: c.data.startswith("third"),
                                       state=FSM_start_survey.compare_answers)
