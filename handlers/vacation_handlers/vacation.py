import os
import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot, db
from dicts.messages import commands_dict
from func.all_func import delete_temp_file
from keyboards.inline_initiate_vacation import yes_no_keyboard, start_sending_vacation_email_keyboard, \
    start_sending_vacation_email_keyboard_o
from mailing.mailing import send_vacation_email


# @dp.callback_query_handler(lambda c: c.data.startswith("vacation"), state=None)
async def vacation(callback_query: types.CallbackQuery):
    type_of_employment = db.what_type_of_employment(callback_query.from_user.id)
    if type_of_employment:
        if type_of_employment == "штат":
            if callback_query.data.split(" ")[1] == "more":
                await callback_query.answer()
                await callback_query.message.answer(commands_dict["vacation"]["vacation_more_two_weeks"],
                                                    reply_markup=start_sending_vacation_email_keyboard,
                                                    parse_mode=types.ParseMode.HTML)
            elif callback_query.data.split(" ")[1] == "less":
                await callback_query.answer()
                await callback_query.message.answer(commands_dict["vacation"]["vacation_less_two_weeks"],
                                                    reply_markup=start_sending_vacation_email_keyboard_o,
                                                    parse_mode=types.ParseMode.HTML)
        else:
            if callback_query.data.split(" ")[1] == "more":
                await callback_query.answer()
                await callback_query.message.answer(commands_dict["vacation"]["vacation_more_two_weeks_not_state"],
                                                    parse_mode=types.ParseMode.HTML)
            elif callback_query.data.split(" ")[1] == "less":
                await callback_query.answer()
                await callback_query.message.answer(commands_dict["vacation"]["vacation_less_two_weeks_not_state"],
                                                    reply_markup=start_sending_vacation_email_keyboard_o,
                                                    parse_mode=types.ParseMode.HTML)
        if callback_query.data.split(" ")[1] == "pay_info":
            await callback_query.answer()
            await callback_query.message.answer(commands_dict["vacation"]["vacation_pay"],
                                                parse_mode=types.ParseMode.HTML)
    else:
        await callback_query.answer()
        await callback_query.message.answer("Не указан тип трудоустройства",
                                            parse_mode=types.ParseMode.HTML)


# Состояния для пересылки письма об отпуске ----------------------------------------------------------------------------
class FSM_send_vacation_email(StatesGroup):
    enter_vacation_period = State()
    is_agreed = State()
    send_doc = State()
    enter_coordinator = State()
    what_type_of_employement = State()


# @dp.callback_query_handler(lambda c: c.data.startswith("initiate"), state=None)
async def initiate_vacation_email(callback_query: types.CallbackQuery, state=None):
    await callback_query.answer()
    sender_tg_id = callback_query.from_user.id
    sender = db.find_contacts_by_tg_id(sender_tg_id)
    async with state.proxy() as data:
        data["from_tg_id"] = sender_tg_id
        data["from_name"] = sender["first_name"]
        data["from_surname"] = sender["surname"]
        data["job_title"] = sender["job_title"]
    await FSM_send_vacation_email.enter_vacation_period.set()
    await bot.send_message(chat_id=callback_query.from_user.id, text="В какие сроки планируется отпуск?: ")


# @dp.message_handler(state=FSM_send_vacation_email.enter_vacation_period)
async def save_vacaton_period(message: types.Message, state=FSMContext):
    await FSM_send_vacation_email.is_agreed.set()
    async with state.proxy() as data:
        data["vacation_period"] = message.text
    await bot.send_message(chat_id=message.from_user.id, text="Отпуск согласован с руководителем?: ",
                           reply_markup=yes_no_keyboard)


# @dp.callback_query_handler(lambda c: c.data.startswith("answer"), state=FSM_send_vacation_email.is_agreed)
async def save_is_agreed(callback_query: types.CallbackQuery, state=FSMContext):
    if callback_query.data.split(" ")[1] == "yes":
        await callback_query.answer()
        await FSM_send_vacation_email.send_doc.set()
        async with state.proxy() as data:
            data["is_agreed"] = "Да"
        await bot.send_message(chat_id=callback_query.from_user.id, text="Пришлите фото заполненного заявления: ")
    else:
        await state.finish()
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Перед отправкой заявления отпуск обязательно надо согласовать.\n"
                                    "Пожалуйста, согласуйте отпуск со своим руководителем")


# @dp.message_handler(content_types="photo", state=FSM_send_vacation_email.send_doc)
async def save_doc(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        await FSM_send_vacation_email.enter_coordinator.set()
        destination = os.getcwd() + "/temp_saves/" + data["from_name"] + " " + data["from_surname"] + ".jpg"
        data["image_path"] = destination
        await message.photo[-1].download(destination_file=destination)
    await bot.send_message(chat_id=message.from_user.id, text="Кто ваш координатор в ТИМ ФОРС: ")


# @dp.message_handler(state=FSM_send_vacation_email.enter_coordinator)
async def save_coordinator(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["coordinator"] = message.text
    from_name = data["from_name"]
    from_surname = data["from_surname"]
    job_title = data["job_title"]
    vacation_period = data["vacation_period"]
    is_agreed = data["is_agreed"]
    coordinator_name = data["coordinator"]
    image_path = data["image_path"]
    is_ok = asyncio.create_task(send_vacation_email(from_name, from_surname, job_title, vacation_period, is_agreed,
                                                    coordinator_name, image_path))
    if is_ok:
        text = f"Ваше заявление на отпуск в период {data['vacation_period']} отправлено координатору"
        await asyncio.sleep(10)
        await asyncio.create_task(delete_temp_file(data["image_path"]))
    else:
        text = is_ok
    await bot.send_message(chat_id=message.from_user.id, text=text)
    await state.finish()


def register_handlers_vacation(dp: Dispatcher):
    dp.register_callback_query_handler(vacation, lambda c: c.data.startswith("vacation"), state=None)
    dp.register_callback_query_handler(initiate_vacation_email, lambda c: c.data.startswith("initiate"), state=None)
    dp.register_message_handler(save_vacaton_period, state=FSM_send_vacation_email.enter_vacation_period)
    dp.register_callback_query_handler(save_is_agreed, lambda c: c.data.startswith("answer"),
                                       state=FSM_send_vacation_email.is_agreed)
    dp.register_message_handler(save_doc, content_types="photo", state=FSM_send_vacation_email.send_doc)
    dp.register_message_handler(save_coordinator, state=FSM_send_vacation_email.enter_coordinator)
