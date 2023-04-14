import os
import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from create_bot import dp, bot, db
from dicts.messages import commands_dict
from func.all_func import delete_temp_file
from keyboards.inline_initiate_vacation import yes_no_keyboard, start_sending_vacation_email_keyboard, \
    start_sending_vacation_email_keyboard_o
from keyboards.inline_type_of_employement import type_of_employement_kb
from mailing.mailing import send_vacation_email
from States.states import FSM_send_vacation_email, FSM_type_of_employment


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
        await FSM_type_of_employment.change_type_of_employment.set()
        await callback_query.message.answer("Я не нашел в своей базе тип твоей занятости в компании Тимфорс.\n"
                                            "Укажи пожалуйста ты оформлен в штат или работаешь по ИП/СЗ/ГПХ ?",
                                            reply_markup=type_of_employement_kb,
                                            parse_mode=types.ParseMode.HTML)


# Состояния для пересылки письма об отпуске ----------------------------------------------------------------------------

# @dp.callback_query_handler(lambda c: c.data.startswith("initiate"), state=None)
async def initiate_vacation_email(callback_query: types.CallbackQuery, state=None):
    await callback_query.answer()
    user = db.find_by_tg_id(callback_query.from_user.id)
    user_department = db.find_department_obj_by_user_id(user.id)
    if not user_department:
        await callback_query.message.answer("Для пользователя не указан отдел работы. Обратитесь к администратору.")
        return
    superviser_id = db.find_superviser(user_department.id)
    superviser = db.find_user_by_id(superviser_id)
    superviser_name = f"{superviser.surname} {superviser.first_name} {superviser.middle_name}"
    superviser_mail = db.find_email_by_user_id(superviser_id)
    sender_tg_id = callback_query.from_user.id
    sender = db.find_contacts_by_tg_id(sender_tg_id)
    async with state.proxy() as data:
        data["from_tg_id"] = sender_tg_id
        data["from_name"] = sender["first_name"]
        data["from_surname"] = sender["surname"]
        data["job_title"] = sender["job_title"]
        data["superviser_mail"] = superviser_mail
        data["superviser_name"] = superviser_name
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
        await FSM_send_vacation_email.enter_coordinator.set()
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Прикрепите через скрепку 📎 фото заполненного заявления на отпуск,\n"
                                    "Убедитесь что фото хорошего качества и документ легко читается\n"
                                    "Документ будет отправлен в отдел кадров")
    else:
        await state.finish()
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="🚫 Перед отправкой заявления отпуск обязательно надо согласовать. 🚫\n"
                                    "Пожалуйста, согласуйте отпуск со своим руководителем")


# @dp.message_handler(content_types="photo", state=FSM_send_vacation_email.enter_coordinator)
async def save_coordinator(message: types.Message, state=FSMContext):
    await FSM_send_vacation_email.commit_data.set()
    async with state.proxy() as data:
        destination = os.getcwd() + "/temp_saves/" + data["from_name"] + "_" + data["from_surname"] + ".jpg"
        await message.photo[-1].download(destination_file=destination)
        data["image_path"] = destination
    text = "<b>Заявление на отпуск</b>\n" \
           f"<b>От:</b> {data['from_surname']} {data['from_name']}\n" \
           f"<b>Даты отпуска:</b> {data['vacation_period']}\n" \
           f"<b>Руководитель:</b> {data['superviser_name']}\n" \
           f"<b>Приложение: {data['image_path'].split('/')[2]}</b>\n\n" \
           f"Письмо будет отправлено в отдел кадров и вашему руководителю\n" \
           f"Отправляем ?"
    await message.answer("Вот что получилось:\n\n"
                         f"{text}", parse_mode=types.ParseMode.HTML, reply_markup=yes_no_keyboard)


# @dp.message_handler(state=FSM_send_vacation_email.enter_coordinator)
async def waiting_for_photo(message: types.Message):
    await message.answer("Я жду фаила с фото заявления на отпуск\n"
                         "Пришли фото через скрепку 📎 или используй /stop для выхода")


# @dp.callback_query_handler(lambda c: c.data.startswith("answer"), state=FSM_send_vacation_email.commit_data)
async def commit_data(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    if callback_query.data.split(" ")[1] == "yes":
        await callback_query.message.answer("Отправляю письмо ...")
        async with state.proxy() as data:
            from_name = data["from_name"]
            from_surname = data["from_surname"]
            job_title = data["job_title"]
            vacation_period = data["vacation_period"]
            coordinator_name = data["superviser_name"]
            image_path = data["image_path"]
            superviser_mail = [data["superviser_mail"]]
        is_ok = asyncio.create_task(send_vacation_email(from_name=from_name,
                                                        from_surname=from_surname,
                                                        job_title=job_title,
                                                        vacation_period=vacation_period,
                                                        coordinator_name=coordinator_name,
                                                        superviser_email=superviser_mail,
                                                        image_path=image_path))
        if is_ok:
            text = f"Ваше заявление на отпуск в период {data['vacation_period']} отправлено координатору"
            await asyncio.sleep(3)
            await asyncio.create_task(delete_temp_file(data["image_path"]))
        else:
            text = is_ok
        await bot.send_message(chat_id=callback_query.message.from_user.id, text=text)
        await state.finish()
    elif callback_query.data.split(" ")[1] == "no":
        async with state.proxy() as data:
            await asyncio.create_task(delete_temp_file(data["image_path"]))
        await callback_query.message.answer("Выхожу их функции отправки заявления на отпуск")


def register_handlers_vacation(dp: Dispatcher):
    dp.register_callback_query_handler(vacation, lambda c: c.data.startswith("vacation"), state=None)
    dp.register_callback_query_handler(initiate_vacation_email, lambda c: c.data.startswith("initiate"), state=None)
    dp.register_message_handler(save_vacaton_period, state=FSM_send_vacation_email.enter_vacation_period)
    dp.register_callback_query_handler(save_is_agreed, lambda c: c.data.startswith("answer"),
                                       state=FSM_send_vacation_email.is_agreed)
    dp.register_message_handler(waiting_for_photo, state=FSM_send_vacation_email.enter_coordinator)
    dp.register_message_handler(save_coordinator, content_types="photo",
                                state=FSM_send_vacation_email.enter_coordinator)
    dp.register_callback_query_handler(commit_data,
                                       lambda c: c.data.startswith("answer"), state=FSM_send_vacation_email.commit_data)

