from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot, db

from States.states import FSM_meeting
from keyboards.inline_meeting import meeting_kb


@dp.message_handler(state=FSM_meeting.start)
async def save_header(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["header"] = message.text
    await message.answer("Напишите список участников в формате @member1 @member2 @member3")
    await FSM_meeting.step_2.set()


@dp.message_handler(state=FSM_meeting.step_2)
async def save_contacts(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["contacts"] = message.text
    await message.answer("напишите время в формате дд.мм.гггг **чч:мм**")
    await FSM_meeting.step_3.set()


@dp.message_handler(state=FSM_meeting.step_3)
async def save_date_time(message: types.Message, state: FSMContext):
    # todo нужен валидатор для времени
    async with state.proxy() as data:
        data["time"] = message.text
    text = f"<b>Встреча</b>: {data['header']}\n" \
           f"<b>Приглашенные</b>: {data['contacts']}\n" \
           f"<b>Дата и время</b>: {data['time']}"
    await message.answer(f"Отлично, давай проверим что получилось:\n\n"
                         f"{text}", parse_mode=types.ParseMode.HTML, reply_markup=meeting_kb)
    await FSM_meeting.end.set()


@dp.callback_query_handler(lambda c: c.data.startswith("meeting"), state=FSM_meeting.end)
async def send_invites(callback_query: types.CallbackQuery, state=FSMContext):

    if callback_query.data.split(" ")[1] == "yes":
        pass
    else:
        pass


def register_handlers_meeting(dp: Dispatcher):
    pass