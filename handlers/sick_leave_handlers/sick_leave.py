from create_bot import dp, bot, db
from aiogram import types, Dispatcher

from func.all_func import is_breakes
from keyboards.inline_type_of_employement import type_of_employement_kb

from States.states import FSM_type_of_employment


# @dp.register_callback_query_handler(lambda c: c.data.startswith("sick"))
async def sick_leave_info(cq: types.CallbackQuery):
    await cq.answer()
    type_of_employement = db.what_type_of_employment(cq.from_user.id)
    if type_of_employement:
        if type_of_employement == "штат":
            if cq.data.split(" ")[1] == "info":
                text = db.find_answer_by_answer_id(37).answer_text
                await cq.message.answer(is_breakes(text), parse_mode=types.ParseMode.HTML)
            elif cq.data.split(" ")[1] == "payment":
                text = db.find_answer_by_answer_id(38).answer_text
                await cq.message.answer(is_breakes(text), parse_mode=types.ParseMode.HTML)
        else:
            text = "Для сотрудников вне штата необходимо уведомить договорной отдел"
            await cq.message.answer(is_breakes(text), parse_mode=types.ParseMode.HTML)
    else:
        await FSM_type_of_employment.change_type_of_employment.set()
        await cq.message.answer("Я не нашел в своей базе тип твоей занятости в компании Тимфорс.\n"
                                "Укажи пожалуйста ты оформлен в штат или работаешь по ИП/СЗ/ГПХ ?",
                                reply_markup=type_of_employement_kb,
                                parse_mode=types.ParseMode.HTML)


def register_handlers_sick_leave(dp: Dispatcher):
    dp.register_callback_query_handler(sick_leave_info, lambda c: c.data.startswith("sick"))
