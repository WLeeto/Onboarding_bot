import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from create_bot import dp, bot, db

from States.states import FSM_meeting
from func.scheldule import send_schelduled_message
from keyboards.inline_meeting import meeting_kb

import re
from datetime import datetime
from datetime import timedelta


@dp.message_handler(state=FSM_meeting.start)
async def save_header(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["header"] = message.text
    await message.answer("Напишите список участников в формате @member1 @member2 @member3")
    await FSM_meeting.step_2.set()


@dp.message_handler(state=FSM_meeting.step_2)
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


@dp.message_handler(state=FSM_meeting.step_3)
async def save_date_time(message: types.Message, state: FSMContext):
    pattern = r"((\d\d).(\d\d).(\d\d\d\d))[\s\S]*((\d\d).(\d\d))"
    try:
        year = re.match(pattern, message.text).group(4)
        month = re.match(pattern, message.text).group(3)
        day = re.match(pattern, message.text).group(2)
        hour = re.match(pattern, message.text).group(6)
        minute = re.match(pattern, message.text).group(7)
        inserted_date = datetime(int(year), int(month), int(day), int(hour), int(minute))
        async with state.proxy() as data:
            data["datetime"] = inserted_date

        text = f"<b>Встреча</b>: {data['header']}\n" \
               f"<b>Приглашенные</b>: {', '.join(data['recipient_list'])}\n" \
               f"<b>Дата и время</b>: {day}.{month}.{year} {hour}:{minute}"
        await message.answer(f"Отлично, давай проверим что получилось:\n\n"
                             f"{text}", parse_mode=types.ParseMode.HTML, reply_markup=meeting_kb)
        await FSM_meeting.end.set()
    except AttributeError:
        await message.answer("Не могу обработать дату, убедитесь что дата введена по шаблону: дд.мм.гггг чч:мм\n"
                             "Или используй /stop чтобы прекратить заполнение")


@dp.callback_query_handler(lambda c: c.data.startswith("meeting"), state=FSM_meeting.end)
async def send_invites(callback_query: types.CallbackQuery, scheduler: AsyncIOScheduler, state=FSMContext, ):
    await callback_query.answer()
    if callback_query.data.split(" ")[1] == "yes":
        async with state.proxy() as data:
            datetime = data["datetime"]
            recipient_list = data["recipient_list"]
            header = data["header"]
        found_users = []
        not_found_users = []
        for recipient in recipient_list:
            user = db.find_user_by_telegram_nickname(recipient)
            if user:
                asyncio.create_task(send_schelduled_message(scheduler=scheduler,
                                                            run_date=datetime - timedelta(minutes=5),
                                                            text=f"Напоминаю о собрании:\n"
                                                                 f"{header}",
                                                            chat_id=user.tg_id))
                found_users.append(recipient)
            else:
                not_found_users.append(f"@{user}")
        if found_users:
            await callback_query.message.answer("Сообщение о собрании было отправлено на почту пользователям: "
                                                f"{', '.join(found_users)}")
        if not_found_users:
            await callback_query.message.answer("Вот этих пользователей я не смог найти в БД: "
                                                f"{', '.join(found_users)}")
        await state.finish()
    else:
        await callback_query.message.answer("Давай начнем все с начала\n"
                                            "Напишите описание встречи и ссылку (если требуется)\n\n"
                                            "Чтобы отменить создание встречи используйте /stop",
                                            parse_mode=types.ParseMode.HTML)
        await FSM_meeting.start.set()


def register_handlers_meeting(dp: Dispatcher):
    pass
