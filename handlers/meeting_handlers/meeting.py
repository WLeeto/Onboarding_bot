import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from create_bot import dp, bot, db

from States.states import FSM_meeting
from func.scheldule import _send_message
from keyboards.inline_meeting import meeting_kb

import re
from datetime import datetime
from datetime import timedelta

from mailing.mailing import send_meeting_email


# @dp.message_handler(state=FSM_meeting.start)
async def save_header(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["header"] = message.text
    await message.answer("Напишите список участников в формате @member1 @member2 @member3")
    await FSM_meeting.step_2.set()


# @dp.message_handler(state=FSM_meeting.step_2)
async def save_contacts(message: types.Message, state: FSMContext):
    pattern_username = r"@\w*"
    pattern_surname = r"[а-яА-ЯёЁ]+"
    username_recipients = re.findall(pattern_username, message.text)
    surname_recipients = re.findall(pattern_surname, message.text)
    recipient_list = username_recipients + surname_recipients
    recipient_id_list = []
    not_found_users = []
    for recipient in recipient_list:
        if recipient.startswith("@"):
            search_flag = db.is_user_by_username(recipient.replace("@", ""))
            if search_flag:
                recipient_id_list.append(str(search_flag.id))
            else:
                not_found_users.append(recipient)
        else:
            search_flag = db.is_user_by_surname(recipient)
            if search_flag:
                for user in search_flag:
                    recipient_id_list.append(str(user.id))
            else:
                not_found_users.append(recipient)
    if not_found_users:
        await message.answer(f"Я не смог найти в БД следующих пользователей:\n{','.join(not_found_users)}\n"
                             f"Введи список получателей снова")
        return

    if len(recipient_list) != 0:
        async with state.proxy() as data:
            data["recipient_list"] = set(recipient_id_list)
        await message.answer("напишите время в формате дд.мм.гггг чч:мм")
        await FSM_meeting.step_3.set()
    else:
        await message.answer("Не указан ни один получатель\n"
                             "Напишите список участников в формате @member1 @member2 @member3\n"
                             "Вы так же можете указать фамилии приглашенных например "
                             "<code>Виноградов Пушкин Сикорский</code>\n"
                             "Или используйте /stop для выхода", parse_mode=types.ParseMode.HTML)


# @dp.message_handler(state=FSM_meeting.step_3)
async def save_date_time(message: types.Message, state: FSMContext):
    pattern = r"((\d\d).(\d\d).(\d\d\d\d))[\s\S]*((\d\d).(\d\d))"
    try:
        year = re.match(pattern, message.text).group(4)
        month = re.match(pattern, message.text).group(3)
        day = re.match(pattern, message.text).group(2)
        hour = re.match(pattern, message.text).group(6)
        minute = re.match(pattern, message.text).group(7)
        inserted_date = datetime(int(year), int(month), int(day), int(hour), int(minute))
        now = datetime.utcnow() + timedelta(hours=3)
        if inserted_date > now + timedelta(minutes=7):
            async with state.proxy() as data:
                invited_list = []
                for i in data['recipient_list']:
                    invited_list.append(f"{db.find_user_by_id(i).surname} {db.find_user_by_id(i).first_name}")
                data["datetime"] = inserted_date

            invited_text = '\n'.join(invited_list)
            text = f"<b>Встреча</b>:\n {data['header']}\n" \
                   f"<b>Приглашенные</b>:\n {invited_text}\n" \
                   f"<b>Дата и время</b>:\n {day}.{month}.{year} {hour}:{minute}"
            await message.answer(f"Отлично, давай проверим что получилось:\n\n"
                                 f"{text}", parse_mode=types.ParseMode.HTML, reply_markup=meeting_kb)
            await FSM_meeting.end.set()
        else:
            await message.answer("Указана дата в прошлом, либо слишком близко к текущей")
    except AttributeError:
        await message.answer("Не могу обработать дату, убедитесь что дата введена по шаблону: дд.мм.гггг чч:мм\n"
                             "Или используй /stop чтобы прекратить заполнение")


# @dp.callback_query_handler(lambda c: c.data.startswith("meeting"), state=FSM_meeting.end)
async def send_invites(callback_query: types.CallbackQuery, scheduler: AsyncIOScheduler, state=FSMContext, ):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    if callback_query.data.split(" ")[1] == "yes":
        await callback_query.message.answer("Отправляю приглашения ...")
        async with state.proxy() as data:
            send_datetime = data["datetime"]
            recipient_list = data["recipient_list"]
            header = data["header"]
        from_user = db.find_by_tg_id(tg_id=callback_query.from_user.id)
        from_user_id = from_user.id
        full_sender_name = f"{from_user.surname} {from_user.first_name}"
        datetime_to_send = send_datetime.strftime("%d.%m.%Y %H:%M")
        found_users = []
        not_found_users = []
        not_found_emails = []
        text = f"<b>Напоминание о встрече:</b>\n" \
               f"{header}\n" \
               f"{datetime_to_send}"
        for recipient in recipient_list:
            user = db.find_user_by_id(recipient)
            if user:
                user_name = user.first_name
                user_surname = user.surname

                user_id = user.id
                user_tg_id = user.tg_id
                user_tg_name = user.tg_name
                scheduler.add_job(_send_message, trigger="date", run_date=send_datetime - timedelta(minutes=5),
                                  kwargs={"chat_id": user_tg_id,
                                          "text": text},
                                  timezone='Europe/Moscow')
                print(f"Создано новое отложенное событие:\n"
                      f"Время: {datetime_to_send}\n"
                      f"Получатель: {user_tg_name}")
                recipient_email = db.find_email_by_user_id(user_id)
                db.add_scheldulered_message(text=text, from_id=from_user_id, to_id=user_id, date_to_send=send_datetime)
                if recipient_email:
                    asyncio.create_task(send_meeting_email(from_name=full_sender_name,
                                                           title=header,
                                                           date=datetime_to_send,
                                                           recipient=recipient_email))
                    found_users.append(f"{user_surname} {user_name}")
                else:
                    not_found_emails.append(f"{user_surname} {user_name}")
        if found_users:
            found_users_text = '\n'.join(found_users)
            await callback_query.message.answer("Сообщение о собрании было отправлено на почту пользователям: "
                                                f"{found_users_text}")
        if not_found_users:
            not_found_users_text = '\n'.join(not_found_users)
            await callback_query.message.answer("Вот этих пользователей я не смог найти в БД: "
                                                f"{not_found_users_text}")
        if not_found_emails:
            not_found_emails_text = '\n'.join(not_found_users)
            await callback_query.message.answer("Вот у этих пользователей не указана почта:\n"
                                                "(им придет только оповещения за 5 минут до встречи)"
                                                f"{not_found_emails_text}")
        await state.finish()
    else:
        await callback_query.message.answer("Давай начнем все с начала\n"
                                            "Напишите описание встречи и ссылку (если требуется)\n\n"
                                            "Чтобы отменить создание встречи используйте /stop",
                                            parse_mode=types.ParseMode.HTML)
        await FSM_meeting.start.set()


def register_handlers_meeting(dp: Dispatcher):
    dp.register_message_handler(save_header, state=FSM_meeting.start)
    dp.register_message_handler(save_contacts, state=FSM_meeting.step_2)
    dp.register_message_handler(save_date_time, state=FSM_meeting.step_3)
    dp.register_callback_query_handler(send_invites, lambda c: c.data.startswith("meeting"), state=FSM_meeting.end)
