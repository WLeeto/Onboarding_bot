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
    pattern = r"@(\w*)"
    recipient_list = re.findall(pattern, message.text)
    if len(recipient_list) != 0:
        async with state.proxy() as data:
            data["recipient_list"] = recipient_list
        await message.answer("напишите время в формате дд.мм.гггг **чч:мм**")
        await FSM_meeting.step_3.set()
    else:
        await message.answer("Не указан ни один получатель\n"
                             "Напишите список участников в формате @member1 @member2 @member3\n"
                             "Или используйте /stop для выхода")


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
        print(now)
        print(inserted_date)
        if inserted_date > now + timedelta(minutes=7):
            async with state.proxy() as data:
                data["datetime"] = inserted_date

            text = f"<b>Встреча</b>: {data['header']}\n" \
                   f"<b>Приглашенные</b>: {', '.join(data['recipient_list'])}\n" \
                   f"<b>Дата и время</b>: {day}.{month}.{year} {hour}:{minute}"
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
    await callback_query.answer()
    if callback_query.data.split(" ")[1] == "yes":
        await callback_query.message.answer("Отправляю приглашения ...")
        async with state.proxy() as data:
            send_datetime = data["datetime"]
            recipient_list = data["recipient_list"]
            header = data["header"]
        from_user = db.find_by_tg_id(tg_id=callback_query.from_user.id)
        full_sender_name = f"{from_user.surname} {from_user.first_name}"
        datetime_to_send = send_datetime.strftime("%d.%m.%Y %H:%M")
        found_users = []
        not_found_users = []
        not_found_emails = []
        text = f"<b>Напоминание о встрече:</b>\n" \
               f"{header}\n" \
               f"{datetime_to_send}"
        for recipient in recipient_list:
            user = db.find_user_by_telegram_nickname(recipient)
            if user:
                scheduler.add_job(_send_message, trigger="date", run_date=send_datetime, args=(user.tg_id, text),
                                  timezone='Europe/Moscow')
                recipient_email = db.find_email_by_user_id(user.id)
                if recipient_email:
                    asyncio.create_task(send_meeting_email(from_name=full_sender_name,
                                                           title=header,
                                                           date=datetime_to_send,
                                                           recipient=recipient_email))
                    found_users.append(recipient)
                else:
                    not_found_emails.append(recipient)
            else:
                not_found_users.append(recipient)
        if found_users:
            await callback_query.message.answer("Сообщение о собрании было отправлено на почту пользователям: "
                                                f"{', '.join(found_users)}")
        if not_found_users:
            await callback_query.message.answer("Вот этих пользователей я не смог найти в БД: "
                                                f"{', '.join(not_found_users)}")
        if not_found_emails:
            await callback_query.message.answer("Вот у этих пользователей не указана почта:\n"
                                                "(им придет только оповещения за 5 минут до встречи)"
                                                f"{', '.join(not_found_emails)}")
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
