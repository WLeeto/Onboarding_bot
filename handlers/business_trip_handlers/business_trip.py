import asyncio
import os

from create_bot import dp, bot, db
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from States.states import FSM_business_trip_form_sending

from dicts.messages import message_dict
from func.all_func import delete_temp_file
from keyboards.inline_biz_trip import biz_trip_form_send_kb
from mailing.mailing import send_biz_trip_email


# @dp.callback_query_handler(lambda c: c.data.startswith("start_bt_form"))
async def business_trip_form_start(callback_query: types.CallbackQuery):
    await callback_query.answer()
    if db.is_user(callback_query.from_user.id):
        await FSM_business_trip_form_sending.start_business_trip_form.set()
        await callback_query.message.answer("Давай заполним форму на командировку, а я отправлю ее в отдел кадров\n"
                                            "Для выхода из заполнения (без отправки) введи /stop\n\n"
                                            "<b>Введи цель поездки:</b>", parse_mode=types.ParseMode.HTML)
    else:
        await callback_query.message.answer(message_dict["not_in_db"])


# @dp.message_handler(state=FSM_business_trip_form_sending.start_business_trip_form)
async def save_bt_purpose(message: types.Message, state=FSMContext):
    await FSM_business_trip_form_sending.enter_dates.set()
    async with state.proxy() as data:
        data["purpose"] = message.text
        data["from_name"] = db.find_by_tg_id(message.from_id).first_name
        data["from_surname"] = db.find_by_tg_id(message.from_id).surname
    await message.answer("Отлично, теперь введи даты командировки:")


# @dp.message_handler(state=FSM_business_trip_form_sending.enter_dates)
async def save_bt_dates(message: types.Message, state=FSMContext):
    await FSM_business_trip_form_sending.save_note.set()
    async with state.proxy() as data:
        data["dates"] = message.text
    await message.answer("Замечательно. Прикрепи фото заполненной служебной записки (просто перетащи сюда):")


# @dp.message_handler(content_types="photo", state=FSM_business_trip_form_sending.save_note)
async def save_note(message: types.Message, state=FSMContext):
    await FSM_business_trip_form_sending.save_advance.set()
    async with state.proxy() as data:
        destination = os.getcwd() + "/temp_saves/bt/"\
                      + data["from_name"] + "_" + data["from_surname"] + "_" + "bt_note" + ".jpg"
        data["note_path"] = destination
        await message.photo[-1].download(destination_file=destination)
    await message.answer("Ок. Теперь прикрепи фото заявления на выдачу аванса (просто перетащи сюда):")


# @dp.message_handler(content_types="photo", state=FSM_business_trip_form_sending.save_advance)
async def save_advance(message: types.Message, state=FSMContext):
    await FSM_business_trip_form_sending.save_tickets.set()
    async with state.proxy() as data:
        destination = os.getcwd() + "/temp_saves/bt/"\
                      + data["from_name"] + "_" + data["from_surname"] + "_" + "advance" + ".jpg"
        data["advance_path"] = destination
        await message.photo[-1].download(destination_file=destination)
    await message.answer("Ок. Теперь прикрепи скан билетов (тоже тащи сюда):")


# @dp.message_handler(content_types="photo", state=FSM_business_trip_form_sending.save_tickets)
async def save_tickets(message: types.Message, state=FSMContext):
    await FSM_business_trip_form_sending.save_checks.set()
    async with state.proxy() as data:
        destination = os.getcwd() + "/temp_saves/bt/" \
                      + data["from_name"] + "_" + data["from_surname"] + "_" + "tickets" + ".jpg"
        data["tickets_path"] = destination
        await message.photo[-1].download(destination_file=destination)
    await message.answer("Ок. Осталось прикрепить фото чеков об оплате (билеты, гостиница):")


# @dp.message_handler(content_types="photo", state=FSM_business_trip_form_sending.save_checks)
async def save_checks(message: types.Message, state=FSMContext):
    await FSM_business_trip_form_sending.send_form.set()
    async with state.proxy() as data:
        destination = os.getcwd() + "/temp_saves/bt/" \
                      + data["from_name"] + "_" + data["from_surname"] + "_" + "checks" + ".jpg"
        data["checks_path"] = destination
        await message.photo[-1].download(destination_file=destination)
        text = "Давай проверим запрос перед отправкой:\n\n" \
               f"В командировку направляется сотрудник: {data['from_name']} {data['from_surname']}\n" \
               f"Цель поездки: {data['purpose']}\n" \
               f"Дата поездки: {data['dates']}\n" \
               f"+ прикрепленные документы\n\n" \
               f"Все верно ?"
    await message.answer(text, reply_markup=biz_trip_form_send_kb)


# @dp.callback_query_handler(lambda c: c.data.startswith("form"), state=FSM_business_trip_form_sending.send_form)
async def form_confirm(callback_query: types.CallbackQuery, state=FSMContext):
    await callback_query.answer()
    if callback_query.data.split(" ")[1] == "True":
        await callback_query.message.answer("Отправляю письмо о командировке")
        async with state.proxy() as data:
            sending = asyncio.create_task(send_biz_trip_email(
                name=data['from_name'],
                surname=data['from_surname'],
                purpose=data['purpose'],
                dates=data['dates'],
                note_path=data['note_path'],
                advance_path=data['advance_path'],
                tickets_path=data['tickets_path'],
                checks_path=data['checks_path'])
            )
        if sending:
            await state.finish()
            await callback_query.message.answer("Сообщение отправлено, доставлено, все ок")
            await asyncio.sleep(5)
            await asyncio.create_task(delete_temp_file(data["note_path"]))
            await asyncio.create_task(delete_temp_file(data["advance_path"]))
            await asyncio.create_task(delete_temp_file(data["tickets_path"]))
            await asyncio.create_task(delete_temp_file(data["checks_path"]))
        else:
            await callback_query.message.answer("Я не смог отправить сообщение, обратитесь к администратору")
    else:
        await FSM_business_trip_form_sending.start_business_trip_form.set()
        await callback_query.message.answer("Ну давай тогда заново.\n\n"
                                            "Введите цель поездки:")


def register_handlers_business_trip(dp: Dispatcher):
    dp.register_callback_query_handler(business_trip_form_start, lambda c: c.data.startswith("start_bt_form"))
    dp.register_message_handler(save_bt_purpose, state=FSM_business_trip_form_sending.start_business_trip_form)
    dp.register_message_handler(save_bt_dates, state=FSM_business_trip_form_sending.enter_dates)
    dp.register_message_handler(save_note, content_types="photo", state=FSM_business_trip_form_sending.save_note)
    dp.register_message_handler(save_advance, content_types="photo", state=FSM_business_trip_form_sending.save_advance)
    dp.register_message_handler(save_tickets, content_types="photo", state=FSM_business_trip_form_sending.save_tickets)
    dp.register_message_handler(save_checks, content_types="photo", state=FSM_business_trip_form_sending.save_checks)
    dp.register_callback_query_handler(form_confirm,
                                       lambda c: c.data.startswith("form"),
                                       state=FSM_business_trip_form_sending.send_form)

