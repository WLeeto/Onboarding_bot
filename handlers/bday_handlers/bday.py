from aiogram import Dispatcher, types
from create_bot import dp, bot, db
from dicts.messages import all_monthes


# @dp.callback_query_handler(lambda c: c.data.startswith("bday"))
async def display_bday(callback_query: types.CallbackQuery):
    month = callback_query.data.split(" ")[1]
    month_number = all_monthes[month][0]
    list_of_users = db.get_users_by_birth_month(month_number)
    if len(list_of_users) > 0:
        text = f"<u><i>В {all_monthes[month][1]} ДР у сотрудников:</i></u>\n"
        for i in list_of_users:
            name = i.first_name
            surname = i.surname
            if i.middle_name is not None:
                middle_name = i.middle_name
            else:
                middle_name = ""
            text += f"{surname} {name} {middle_name} - {i.date_of_birth.strftime('%d.%m')}\n"
    else:
        text = f"В БД нет сотрудников с ДР в {all_monthes[month][1]}"

    await callback_query.message.edit_text(text, reply_markup=None, parse_mode=types.ParseMode.HTML)


def register_handlers_bday(dp: Dispatcher):
    dp.register_callback_query_handler(display_bday, lambda c: c.data.startswith("bday"))