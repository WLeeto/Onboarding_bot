import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from pprint import pprint

from States.states import FSM_newbie_xlsx
from create_bot import dp, bot, db
from dicts.messages import expense_center_xlsx_dict, business_role_xlsx_dict
from func.all_func import is_breakes, delete_temp_file, list_split, create_pagi_data
from func.create_xlsx import create_newbie_xlsx
from keyboards.inline_xlsx_newbie_form import create_kb, create_kb_next, create_kb_mid, create_kb_prev
from mailing.mailing import send_create_corp_email


# todo собрать весь повторяющийся код (пагинатор и other) в отдельные функции


@dp.callback_query_handler(lambda c: c.data == "xlsx_start")
async def start_xlsx_creating(callback_query: types.CallbackQuery, state: FSMContext):
    await FSM_newbie_xlsx.step_1.set()
    await callback_query.answer()
    await callback_query.message.answer("Тестовые данные для формирования xlsx фаила:\n"
                                        "ФИО: Пупкин Владимир Владимирович\n"
                                        "Фамилия на английском: Pupkin\n"
                                        "Дата рождения: 26.06.1966\n"
                                        "Телефон: +79158548483\n"
                                        "Email: pupkin@mail.ru\n"
                                        "Руководитель: Гайнанова Роза Ильшотовна")
    button_list = ["ООО «СмартСтаффинг»", "ООО «ТИМ ФОРС»", "ООО «ТИМ ФОРС Сервис»", "ООО «ТИМ ФОРС Менеджмент»",
                   "ООО «ТАТМобайлИнформ СиДиСи»", 'ООО "Репола"', 'ООО "Сириус"', 'ООО "Кайрос"', 'ООО "Бивень"',
                   "Другое (Ввести вручную)"]
    cbq_list = ["ООО «СмартСтаффинг»", "ООО «ТИМ ФОРС»", "ООО «ТИМ ФОРС Сервис»", "ООО «ТИМ ФОРС Менеджмент»",
                "ООО «ТАТМобайлИнформ СиДиСи»", 'ООО "Репола"', 'ООО "Сириус"', 'ООО "Кайрос"', 'ООО "Бивень"',
                "Другое"]
    button_list_list = list_split(button_list, 5)
    cbq_list_list = list_split(cbq_list, 5)
    pagi_data = create_pagi_data(button_list_list, cbq_list_list)
    legal_entity_kb = create_kb_next(buttons_text=button_list[0:5], callback_data=cbq_list[0:5])
    to_edit = await callback_query.message.answer("Выберите ЮЛ:", reply_markup=legal_entity_kb)
    async with state.proxy() as data:
        data["to_edit"] = to_edit
        data["surname"] = "Пупкин"
        data["surname_eng"] = "Pupkin"
        data["name"] = "Владимир"
        data["patronim"] = "Владимирович"
        data["date_of_birth"] = "26.06.1966"
        data["phone"] = "+79158548483"
        data["email"] = "pupkin@mail.ru"
        data["superviser"] = "Гайнанова Роза Ильшотовна"
        data["first_work_day"] = "25.04.2023"
        data["pagi"] = pagi_data
        data["pagi_step"] = 0


@dp.callback_query_handler(lambda c: c.data.startswith("xlsx_pagi"), state=FSM_newbie_xlsx.step_1)
async def xlsx_pagi(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback_query.data.split(" ")[1] == "next":
            data["pagi_step"] += 1
            step = data["pagi_step"]
            if step + 1 in data["pagi"]["text"]:
                kb = create_kb_mid(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                    message_id=data["to_edit"].message_id,
                                                    reply_markup=kb)
                data["to_edit"] = to_edit
            else:
                kb = create_kb_prev(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                              message_id=data["to_edit"].message_id,
                                                              reply_markup=kb)
                data["to_edit"] = to_edit
        elif callback_query.data.split(" ")[1] == "prev":
            data["pagi_step"] -= 1
            step = data["pagi_step"]
            if step - 1 in data["pagi"]["text"]:
                kb = create_kb_mid(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                              message_id=data["to_edit"].message_id,
                                                              reply_markup=kb)
                data["to_edit"] = to_edit
            else:
                kb = create_kb_next(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                              message_id=data["to_edit"].message_id,
                                                              reply_markup=kb)
                data["to_edit"] = to_edit


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_1)
async def newbie_xlsx_step_1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["legal_entity"] = callback_query.data
        await callback_query.answer()
        button_list = ["Команда", "Проекты", "Другое (Ввести вручную)"]
        cbq_list = ["Команда", "Проекты", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"Тип сотрудника:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_2.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'ЮЛ':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_2)
async def newbie_xlsx_step_2(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["emp_type"] = callback_query.data
        await callback_query.answer()
        button_list = ["Штат", "Внешний", "Другое (Ввести вручную)"]
        cbq_list = ["Штат", "Внешний", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"Формат сотрудничества:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_3.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Тип сотрудника':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_3)
async def newbie_xlsx_step_3(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["type_of_cooperation"] = callback_query.data
        await callback_query.answer()
        button_list = ["Сколково", "Удаленка", "Гибрид", "Другое (Ввести вручную)"]
        cbq_list = ["Сколково", "Удаленка", "Гибрид", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"Офис:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_4.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Формат сотрудничества:':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_4)
async def newbie_xlsx_step_4(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["office"] = callback_query.data
        await callback_query.answer()
        button_list = ["/Блок Проекты", "/Блок Проекты/Группа договорной работы", "/Блок Проекты/Группа координаторов",
                       "/Блок Проекты/Тендерная группа", "/Блок Развитие", "/Блок Ресурсы", "/Блок Ресурсы/Отдел КДП",
                       "/Блок Ресурсы/Отдел рекрутмента", "/Блок Ресурсы/Группа ресурсного менджмента", "/Блок Сервисы",
                       "/Блок Технологии", "/Блок Финансы/Бухгалтерия", "/Блок Финансы/Казначейство",
                       "Другое (Ввести вручную)"]
        cbq_list = ["1", "2", "3",
                    "4", "5", "6", "7",
                    "8", "9", "10",
                    "11", "12", "13", "Другое"]

        button_list_list = list_split(button_list, 5)
        cbq_list_list = list_split(cbq_list, 5)
        pagi_data = create_pagi_data(button_list_list, cbq_list_list)

        legal_entity_kb = create_kb_next(buttons_text=button_list[0:5], callback_data=cbq_list[0:5], row_width=2)
        to_edit = await bot.edit_message_text(f"Центр расходов:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
            data["pagi"] = pagi_data
            data["pagi_step"] = 0
        await FSM_newbie_xlsx.step_5.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Офис':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(lambda c: c.data.startswith("xlsx_pagi"), state=FSM_newbie_xlsx.step_5)
async def xlsx_pagi(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback_query.data.split(" ")[1] == "next":
            data["pagi_step"] += 1
            step = data["pagi_step"]
            if step + 1 in data["pagi"]["text"]:
                kb = create_kb_mid(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                    message_id=data["to_edit"].message_id,
                                                    reply_markup=kb)
                data["to_edit"] = to_edit
            else:
                kb = create_kb_prev(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                              message_id=data["to_edit"].message_id,
                                                              reply_markup=kb)
                data["to_edit"] = to_edit
        elif callback_query.data.split(" ")[1] == "prev":
            data["pagi_step"] -= 1
            step = data["pagi_step"]
            if step - 1 in data["pagi"]["text"]:
                kb = create_kb_mid(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                              message_id=data["to_edit"].message_id,
                                                              reply_markup=kb)
                data["to_edit"] = to_edit
            else:
                kb = create_kb_next(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                              message_id=data["to_edit"].message_id,
                                                              reply_markup=kb)
                data["to_edit"] = to_edit


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_5)
async def newbie_xlsx_step_5(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["expense_center"] = expense_center_xlsx_dict[f"{callback_query.data}"]
        await callback_query.answer()
        button_list = ["Основатель", "Операционный директор", "Директор программы", "Директор блока", "Лидер группы",
                       "Руководитель проектов", "Аккаунт-менеджер", "Специалист по договорной работе",
                       "Тендерный специалист", "Координатор проектов", "Партнерский менеджер", "Специалист КДП",
                       "Рекрутер", "Ресурсный менеджер", "Менеджер", "Руководитель ИТ-службы", "Юрист",
                       "Менеджер продукта",
                       "Разработчик B2BCloud", "Бухгалтер по основной деятельности", "Бухгалтер",
                       "Бухгалтер по вспомогательной деятельности", "Бухгалтер по расчету заработной платы",
                       "Главный бухгалтер", "Бухгалтер-операционист", "Финансовый менджер", "Стажер", "Разработчик PHP",
                       "Разработчик JS", "Тестировщик", "Python разработчик", "Ассистент отдела развития",
                       "Другое (Ввести вручную)"]
        cbq_list = ["1", "2", "3", "4", "5",
                    "6", "7", "8",
                    "9", "10", "11", "12",
                    "13", "14", "15", "16", "17", "18",
                    "19", "20", "21",
                    "22", "23",
                    "24", "25", "26", "27", "28",
                    "29", "30", "31", "32", "Другое"]

        button_list_list = list_split(button_list, 5)
        cbq_list_list = list_split(cbq_list, 5)
        pagi_data = create_pagi_data(button_list_list, cbq_list_list)

        legal_entity_kb = create_kb(buttons_text=button_list[0:5], callback_data=cbq_list[0:5], row_width=4)
        to_edit = await bot.edit_message_text(f"Бизнес-роль:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
            data["pagi"] = pagi_data
            data["pagi_step"] = 0
        await FSM_newbie_xlsx.step_6.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Центр расходов':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(lambda c: c.data.startswith("xlsx_pagi"), state=FSM_newbie_xlsx.step_6)
async def xlsx_pagi(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback_query.data.split(" ")[1] == "next":
            data["pagi_step"] += 1
            step = data["pagi_step"]
            if step + 1 in data["pagi"]["text"]:
                kb = create_kb_mid(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                    message_id=data["to_edit"].message_id,
                                                    reply_markup=kb)
                data["to_edit"] = to_edit
            else:
                kb = create_kb_prev(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                              message_id=data["to_edit"].message_id,
                                                              reply_markup=kb)
                data["to_edit"] = to_edit
        elif callback_query.data.split(" ")[1] == "prev":
            data["pagi_step"] -= 1
            step = data["pagi_step"]
            if step - 1 in data["pagi"]["text"]:
                kb = create_kb_mid(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                              message_id=data["to_edit"].message_id,
                                                              reply_markup=kb)
                data["to_edit"] = to_edit
            else:
                kb = create_kb_next(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                              message_id=data["to_edit"].message_id,
                                                              reply_markup=kb)
                data["to_edit"] = to_edit


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_6)
async def newbie_xlsx_step_6(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["business_role"] = business_role_xlsx_dict[f"{callback_query.data}"]
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"Удаленный доступ:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_7.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Бизнес-роль':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_7)
async def newbie_xlsx_step_7(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["Удаленный доступ"] = callback_query.data
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"<b>Информационные ресурсы</b> БУХ:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id,
                                              parse_mode=types.ParseMode.HTML)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_8.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Удаленный доступ':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_8)
async def newbie_xlsx_step_8(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["БУХ"] = callback_query.data
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"<b>Информационные ресурсы</b> ЗУП:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id,
                                              parse_mode=types.ParseMode.HTML)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_9.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'БУХ':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_9)
async def newbie_xlsx_step_9(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["ЗУП"] = callback_query.data
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"<b>Информационные ресурсы</b> ДОК:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id,
                                              parse_mode=types.ParseMode.HTML)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_10.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'ЗУП':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_10)
async def newbie_xlsx_step_10(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["ДОК"] = callback_query.data
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"<b>Информационные ресурсы</b> СБИС:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id,
                                              parse_mode=types.ParseMode.HTML)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_11.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'ДОК':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_11)
async def newbie_xlsx_step_11(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["СБИС"] = callback_query.data
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"<b>Файловые ресурсы</b> Public:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id,
                                              parse_mode=types.ParseMode.HTML)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_12.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'СБИС':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_12)
async def newbie_xlsx_step_12(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["Public"] = callback_query.data
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"<b>Файловые ресурсы</b> Findoc:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id,
                                              parse_mode=types.ParseMode.HTML)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_13.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Public':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_13)
async def newbie_xlsx_step_13(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["Findoc"] = callback_query.data
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"<b>Файловые ресурсы</b> КДП:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id,
                                              parse_mode=types.ParseMode.HTML)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_14.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Findoc':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_14)
async def newbie_xlsx_step_14(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["КДП"] = callback_query.data
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"<b>Файловые ресурсы</b> FindocBK:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id,
                                              parse_mode=types.ParseMode.HTML)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_15.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'КДП':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_15)
async def newbie_xlsx_step_15(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["FindocBK"] = callback_query.data
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"<b>Внешние сервисы</b> Контур Фокус:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id,
                                              parse_mode=types.ParseMode.HTML)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_16.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'FindocBK':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_16)
async def newbie_xlsx_step_16(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["Контур Фокус"] = callback_query.data
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"<b>Внешние сервисы</b> Бикотендер:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id,
                                              parse_mode=types.ParseMode.HTML)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_17.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Контур Фокус':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_17)
async def newbie_xlsx_step_17(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["Бикотендер"] = callback_query.data
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"<b>Внешние сервисы</b> Консультант+:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id,
                                              parse_mode=types.ParseMode.HTML)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_18.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Бикотендер':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_18)
async def newbie_xlsx_step_18(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["Консультант+"] = callback_query.data
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"Доступ 1С:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_19.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Консультант+':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_19)
async def newbie_xlsx_step_19(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["Доступ 1С"] = callback_query.data
        await callback_query.answer()
        button_list = ["teamforce.ru", "teamforce.dev", "Другое (Ввести вручную)"]
        cbq_list = ["teamforce.ru", "teamforce.dev", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"Домен почты:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_20.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Доступ 1С':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_20)
async def newbie_xlsx_step_20(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["Домен почты"] = callback_query.data
        await callback_query.answer()
        button_list = ["smartstaffing.ru", "tatmobile.solutions", "repola.dev", "sirius.engineering",
                       "Другое (Ввести вручную)"]
        cbq_list = ["smartstaffing.ru", "tatmobile.solutions", "repola.dev", "sirius.engineering", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"Дополнительный домен почты:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_21.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Домен почты':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_21)
async def newbie_xlsx_step_21(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["Дополнительный домен почты"] = callback_query.data
        await callback_query.answer()
        button_list = ["group_general@teamforce.ru", "group_buh@teamforce.ru", "group_contracts@teamforce.ru",
                       "group_treasury@teamforce.ru", "group_kdp@teamforce.ru", "group_coordination@teamforce.ru",
                       "group_development@teamforce.ru", "group_recruitment@teamforce.ru",
                       "group_resource-management@teamforce.ru", "group_services@teamforce.ru",
                       "group_tech@teamforce.ru",
                       "group_tenders@teamforce.ru", "partnership@teamforce.ru", "team@teamforce.ru",
                       "Другое (Ввести вручную)"]
        cbq_list = ["group_general@teamforce.ru", "group_buh@teamforce.ru", "group_contracts@teamforce.ru",
                    "group_treasury@teamforce.ru", "group_kdp@teamforce.ru", "group_coordination@teamforce.ru",
                    "group_development@teamforce.ru", "group_recruitment@teamforce.ru",
                    "group_resource-management@teamforce.ru", "group_services@teamforce.ru", "group_tech@teamforce.ru",
                    "group_tenders@teamforce.ru", "partnership@teamforce.ru", "team@teamforce.ru", "Другое"]

        button_list_list = list_split(button_list, 5)
        cbq_list_list = list_split(cbq_list, 5)
        pagi_data = create_pagi_data(button_list_list, cbq_list_list)

        legal_entity_kb = create_kb_next(buttons_text=button_list[0:5], callback_data=cbq_list[0:5])
        to_edit = await bot.edit_message_text(f"Основная группа (только для команды):", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
            data["pagi"] = pagi_data
            data["pagi_step"] = 0
        await FSM_newbie_xlsx.step_22.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Дополнительный домен почты':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(lambda c: c.data.startswith("xlsx_pagi"), state=FSM_newbie_xlsx.step_22)
async def xlsx_pagi(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback_query.data.split(" ")[1] == "next":
            data["pagi_step"] += 1
            step = data["pagi_step"]
            if step + 1 in data["pagi"]["text"]:
                kb = create_kb_mid(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                    message_id=data["to_edit"].message_id,
                                                    reply_markup=kb)
                data["to_edit"] = to_edit
            else:
                kb = create_kb_prev(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                              message_id=data["to_edit"].message_id,
                                                              reply_markup=kb)
                data["to_edit"] = to_edit
        elif callback_query.data.split(" ")[1] == "prev":
            data["pagi_step"] -= 1
            step = data["pagi_step"]
            if step - 1 in data["pagi"]["text"]:
                kb = create_kb_mid(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                              message_id=data["to_edit"].message_id,
                                                              reply_markup=kb)
                data["to_edit"] = to_edit
            else:
                kb = create_kb_next(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                              message_id=data["to_edit"].message_id,
                                                              reply_markup=kb)
                data["to_edit"] = to_edit


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_22)
async def newbie_xlsx_step_22(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["Основная группа"] = callback_query.data
        await callback_query.answer()
        button_list = ["нет", "group_general@teamforce.ru", "group_buh@teamforce.ru", "group_contracts@teamforce.ru",
                       "group_treasury@teamforce.ru", "group_kdp@teamforce.ru", "group_coordination@teamforce.ru",
                       "group_development@teamforce.ru", "group_recruitment@teamforce.ru",
                       "group_resource-management@teamforce.ru", "group_services@teamforce.ru",
                       "group_tech@teamforce.ru",
                       "group_tenders@teamforce.ru", "partnership@teamforce.ru", "team@teamforce.ru",
                       "Другое (Ввести вручную)"]
        cbq_list = ["нет", "group_general@teamforce.ru", "group_buh@teamforce.ru", "group_contracts@teamforce.ru",
                    "group_treasury@teamforce.ru", "group_kdp@teamforce.ru", "group_coordination@teamforce.ru",
                    "group_development@teamforce.ru", "group_recruitment@teamforce.ru",
                    "group_resource-management@teamforce.ru", "group_services@teamforce.ru", "group_tech@teamforce.ru",
                    "group_tenders@teamforce.ru", "partnership@teamforce.ru", "team@teamforce.ru", "Другое"]

        button_list_list = list_split(button_list, 5)
        cbq_list_list = list_split(cbq_list, 5)
        pagi_data = create_pagi_data(button_list_list, cbq_list_list)

        legal_entity_kb = create_kb(buttons_text=button_list[0:5], callback_data=cbq_list[0:5])
        to_edit = await bot.edit_message_text(f"Другие группы:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
            data["pagi"] = pagi_data
            data["pagi_step"] = 0
        await FSM_newbie_xlsx.step_23.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer(
            "Введите значение для поля 'Основная группа (только для команды)':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(lambda c: c.data.startswith("xlsx_pagi"), state=FSM_newbie_xlsx.step_23)
async def xlsx_pagi(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback_query.data.split(" ")[1] == "next":
            data["pagi_step"] += 1
            step = data["pagi_step"]
            if step + 1 in data["pagi"]["text"]:
                kb = create_kb_mid(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                    message_id=data["to_edit"].message_id,
                                                    reply_markup=kb)
                data["to_edit"] = to_edit
            else:
                kb = create_kb_prev(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                              message_id=data["to_edit"].message_id,
                                                              reply_markup=kb)
                data["to_edit"] = to_edit
        elif callback_query.data.split(" ")[1] == "prev":
            data["pagi_step"] -= 1
            step = data["pagi_step"]
            if step - 1 in data["pagi"]["text"]:
                kb = create_kb_mid(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                              message_id=data["to_edit"].message_id,
                                                              reply_markup=kb)
                data["to_edit"] = to_edit
            else:
                kb = create_kb_next(buttons_text=data["pagi"]["text"][step], callback_data=data["pagi"]["cbq"][step])
                to_edit = await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                                              message_id=data["to_edit"].message_id,
                                                              reply_markup=kb)
                data["to_edit"] = to_edit


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_23)
async def newbie_xlsx_step_23(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["Другие группы"] = callback_query.data
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"<b>Оборудование</b> Ноутбук:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id,
                                              parse_mode=types.ParseMode.HTML)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_24.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Другие группы':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_24)
async def newbie_xlsx_step_24(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["Ноутбук"] = callback_query.data
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"<b>Оборудование</b> Внешний монитор:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id,
                                              parse_mode=types.ParseMode.HTML)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_25.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Ноутбук':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_25)
async def newbie_xlsx_step_25(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["Внешний монитор"] = callback_query.data
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"<b>Оборудование</b> Телефон:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id,
                                              parse_mode=types.ParseMode.HTML)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_26.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Внешний монитор':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_26)
async def newbie_xlsx_step_26(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["Телефон"] = callback_query.data
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"<b>Оборудование</b> Флэшка:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id,
                                              parse_mode=types.ParseMode.HTML)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_27.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Телефон':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_27)
async def newbie_xlsx_step_27(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["Флэшка"] = callback_query.data
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"<b>Оборудование</b> Модем:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id,
                                              parse_mode=types.ParseMode.HTML)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.step_28.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Флэшка':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_28)
async def newbie_xlsx_step_28(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["Модем"] = callback_query.data
        await callback_query.answer()
        button_list = ["Да", "Нет", "Другое"]
        cbq_list = ["Да", "Нет", "Другое"]
        legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        to_edit = await bot.edit_message_text(f"<b>Услуги</b> Мобильная связь:", reply_markup=legal_entity_kb,
                                              chat_id=callback_query.from_user.id,
                                              message_id=data["to_edit"].message_id,
                                              parse_mode=types.ParseMode.HTML)
        async with state.proxy() as data:
            data["to_edit"] = to_edit
        await FSM_newbie_xlsx.commit_data.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Модем':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
        await FSM_newbie_xlsx.other.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.commit_data)
async def commit_data(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != "Другое":
        async with state.proxy() as data:
            data["Мобильная связь"] = callback_query.data
            text = "Давай проверим что получилось:\n\n" \
                   f'Фамилия: <code>{data["surname"]}</code>\n' \
                   f'Фамилия (англ.) <code>{data["surname_eng"]}</code>\n' \
                   f'Имя <code>{data["name"]}</code>\n' \
                   f'Отчество <code>{data["patronim"]}</code>\n' \
                   f'День рождения <code>{data["date_of_birth"]}</code>\n' \
                   f'Телефон <code>{data["phone"]}</code>\n' \
                   f'E-mail <code>{data["email"]}</code>\n' \
                   f'ЮЛ <code>{data["legal_entity"]}</code>\n' \
                   f'Тип сотрудника <code>{data["emp_type"]}</code>\n' \
                   f'Формат сотрудничества <code>{data["type_of_cooperation"]}</code>\n' \
                   f'Офис <code>{data["office"]}</code>\n' \
                   f'Дата выхода <code>{data["first_work_day"]}</code>\n' \
                   f'Центр расходов <code>{data["expense_center"]}</code>\n' \
                   f'Руководитель <code>{data["superviser"]}</code>\n' \
                   f'Бизнес-роль <code>{data["business_role"]}</code>\n' \
                   f'Удаленный доступ <code>{data["Удаленный доступ"]}</code>\n\n' \
                   f'<b>Информационные ресурсы</b>\n' \
                   f'БУХ <code>{data["БУХ"]}</code>\n' \
                   f'ЗУП <code>{data["ЗУП"]}</code>\n' \
                   f'ДОК <code>{data["ДОК"]}</code>\n' \
                   f'СБИС <code>{data["СБИС"]}</code>\n\n' \
                   f'<b>Файловые ресурсы</b>\n' \
                   f'Public <code>{data["Public"]}</code>\n' \
                   f'Findoc <code>{data["Findoc"]}</code>\n' \
                   f'КДП <code>{data["КДП"]}</code>\n' \
                   f'FindocBK <code>{data["FindocBK"]}</code>\n\n' \
                   f'Внешние сервисы\n' \
                   f'Контур Фокус <code>{data["Контур Фокус"]}</code>\n' \
                   f'Бикотендер <code>{data["Бикотендер"]}</code>\n' \
                   f'Консультант+ <code>{data["Консультант+"]}</code>\n' \
                   f'Доступ 1С <code>{data["Доступ 1С"]}</code>\n' \
                   f'Домен почты <code>{data["Домен почты"]}</code>\n' \
                   f'Дополнительный домен почты <code>{data["Дополнительный домен почты"]}</code>\n' \
                   f'Основная группа (только для команды) <code>{data["Основная группа"]}</code>\n' \
                   f'Другие группы <code>{data["Другие группы"]}</code>\n\n' \
                   f'<b>Оборудование</b>\n' \
                   f'Ноутбук <code>{data["Ноутбук"]}</code>\n' \
                   f'Внешний монитор <code>{data["Внешний монитор"]}</code>\n' \
                   f'Телефон <code>{data["Телефон"]}</code>\n' \
                   f'Флэшка <code>{data["Флэшка"]}</code>\n' \
                   f'Модем <code>{data["Модем"]}</code>\n\n' \
                   f'<b>Услуги</b>\n' \
                   f'Мобильная связь <code>{callback_query.data}</code>'
        button_list = ["Отправляем", "Редактируем", "Получить xlsx фаил"]
        cbq_list = ["Отправляем", "Редактируем", "Получить xlsx фаил"]
        temp_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        await bot.edit_message_text(text, callback_query.from_user.id, data["to_edit"].message_id, reply_markup=temp_kb,
                                    parse_mode=types.ParseMode.HTML)
        await FSM_newbie_xlsx.finish.set()
    else:
        await callback_query.answer()
        to_del = await callback_query.message.answer("Введите значение для поля 'Мобильная связь':")
        async with state.proxy() as data:
            data["state"] = await state.get_state()
            data["to_del"] = to_del
            print(data["state"])
        await FSM_newbie_xlsx.other.set()


@dp.message_handler(state=FSM_newbie_xlsx.other)
async def newbie_xlsx_other(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        await data["to_del"].delete()
        if data["state"] == "FSM_newbie_xlsx:step_1":
            data["legal_entity"] = message.text
            button_list = ["Команда", "Проекты", "Другое (Ввести вручную)"]
            cbq_list = ["Команда", "Проекты", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"Тип сотрудника:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_2.set()
        elif data["state"] == "FSM_newbie_xlsx:step_2":
            async with state.proxy() as data:
                data["emp_type"] = message.text
            button_list = ["Штат", "Внешний", "Другое (Ввести вручную)"]
            cbq_list = ["Штат", "Внешний", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"Формат сотрудничества:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_3.set()

        elif data["state"] == "FSM_newbie_xlsx:step_3":
            async with state.proxy() as data:
                data["type_of_cooperation"] = message.text
            button_list = ["Сколково", "Удаленка", "Гибрид", "Другое (Ввести вручную)"]
            cbq_list = ["Сколково", "Удаленка", "Гибрид", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"Офис:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_4.set()

        elif data["state"] == "FSM_newbie_xlsx:step_4":
            async with state.proxy() as data:
                data["office"] = message.text
            button_list = ["/Блок Проекты", "/Блок Проекты/Группа договорной работы",
                           "/Блок Проекты/Группа координаторов",
                           "/Блок Проекты/Тендерная группа", "/Блок Развитие", "/Блок Ресурсы",
                           "/Блок Ресурсы/Отдел КДП",
                           "/Блок Ресурсы/Отдел рекрутмента", "/Блок Ресурсы/Группа ресурсного менджмента",
                           "/Блок Сервисы",
                           "/Блок Технологии", "/Блок Финансы/Бухгалтерия", "/Блок Финансы/Казначейство",
                           "Другое (Ввести вручную)"]
            cbq_list = ["1", "2", "3",
                        "4", "5", "6", "7",
                        "8", "9", "10",
                        "11", "12", "13", "Другое"]

            button_list_list = list_split(button_list, 5)
            cbq_list_list = list_split(cbq_list, 5)
            pagi_data = create_pagi_data(button_list_list, cbq_list_list)

            legal_entity_kb = create_kb_next(buttons_text=button_list[0:5], callback_data=cbq_list[0:5], row_width=2)
            to_edit = await bot.edit_message_text(f"Центр расходов:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
                data["pagi"] = pagi_data
                data["pagi_step"] = 0
            await FSM_newbie_xlsx.step_5.set()

        elif data["state"] == "FSM_newbie_xlsx:step_5":
            async with state.proxy() as data:
                data["expense_center"] = message.text
            button_list = ["Основатель", "Операционный директор", "Директор программы", "Директор блока",
                           "Лидер группы",
                           "Руководитель проектов", "Аккаунт-менеджер", "Специалист по договорной работе",
                           "Тендерный специалист", "Координатор проектов", "Партнерский менеджер", "Специалист КДП",
                           "Рекрутер", "Ресурсный менеджер", "Менеджер", "Руководитель ИТ-службы", "Юрист",
                           "Менеджер продукта",
                           "Разработчик B2BCloud", "Бухгалтер по основной деятельности", "Бухгалтер",
                           "Бухгалтер по вспомогательной деятельности", "Бухгалтер по расчету заработной платы",
                           "Главный бухгалтер", "Бухгалтер-операционист", "Финансовый менджер", "Стажер",
                           "Разработчик PHP",
                           "Разработчик JS", "Тестировщик", "Python разработчик", "Ассистент отдела развития",
                           "Другое (Ввести вручную)"]
            cbq_list = ["1", "2", "3", "4", "5",
                        "6", "7", "8",
                        "9", "10", "11", "12",
                        "13", "14", "15", "16", "17", "18",
                        "19", "20", "21",
                        "22", "23",
                        "24", "25", "26", "27", "28",
                        "29", "30", "31", "32", "Другое"]

            button_list_list = list_split(button_list, 5)
            cbq_list_list = list_split(cbq_list, 5)
            pagi_data = create_pagi_data(button_list_list, cbq_list_list)

            legal_entity_kb = create_kb_next(buttons_text=button_list[0:5], callback_data=cbq_list[0:5], row_width=4)
            to_edit = await bot.edit_message_text(f"Бизнес-роль:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
                data["pagi"] = pagi_data
                data["pagi_step"] = 0
            await FSM_newbie_xlsx.step_6.set()

        elif data["state"] == "FSM_newbie_xlsx:step_6":
            async with state.proxy() as data:
                data["business_role"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"Удаленный доступ:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_7.set()

        elif data["state"] == "FSM_newbie_xlsx:step_7":
            async with state.proxy() as data:
                data["Удаленный доступ"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"БУХ:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_8.set()

        elif data["state"] == "FSM_newbie_xlsx:step_8":
            async with state.proxy() as data:
                data["БУХ"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"ЗУП:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_9.set()

        elif data["state"] == "FSM_newbie_xlsx:step_9":
            async with state.proxy() as data:
                data["ЗУП"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"ДОК:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_10.set()

        elif data["state"] == "FSM_newbie_xlsx:step_10":
            async with state.proxy() as data:
                data["ДОК"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"СБИС:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_11.set()

        elif data["state"] == "FSM_newbie_xlsx:step_11":
            async with state.proxy() as data:
                data["СБИС"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"Public:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_12.set()

        elif data["state"] == "FSM_newbie_xlsx:step_12":
            async with state.proxy() as data:
                data["Public"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"Findoc:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_13.set()

        elif data["state"] == "FSM_newbie_xlsx:step_13":
            async with state.proxy() as data:
                data["Findoc"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"КДП:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_14.set()

        elif data["state"] == "FSM_newbie_xlsx:step_14":
            async with state.proxy() as data:
                data["КДП"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"FindocBK:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_15.set()

        elif data["state"] == "FSM_newbie_xlsx:step_15":
            async with state.proxy() as data:
                data["FindocBK"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"Контур Фокус:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_16.set()

        elif data["state"] == "FSM_newbie_xlsx:step_16":
            async with state.proxy() as data:
                data["Контур Фокус"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"Бикотендер:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_17.set()

        elif data["state"] == "FSM_newbie_xlsx:step_17":
            async with state.proxy() as data:
                data["Бикотендер"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"Консультант+:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_18.set()

        elif data["state"] == "FSM_newbie_xlsx:step_18":
            async with state.proxy() as data:
                data["Консультант+"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"Доступ 1С:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_19.set()

        elif data["state"] == "FSM_newbie_xlsx:step_19":
            async with state.proxy() as data:
                data["Доступ 1С"] = message.text
            button_list = ["teamforce.ru", "teamforce.dev", "Другое (Ввести вручную)"]
            cbq_list = ["teamforce.ru", "teamforce.dev", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"Домен почты:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_20.set()

        elif data["state"] == "FSM_newbie_xlsx:step_20":
            async with state.proxy() as data:
                data["Домен почты"] = message.text
            button_list = ["smartstaffing.ru", "tatmobile.solutions", "repola.dev", "sirius.engineering",
                           "Другое (Ввести вручную)"]
            cbq_list = ["smartstaffing.ru", "tatmobile.solutions", "repola.dev", "sirius.engineering", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"Дополнительный домен почты:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_21.set()

        elif data["state"] == "FSM_newbie_xlsx:step_21":
            async with state.proxy() as data:
                data["Дополнительный домен почты"] = message.text
            button_list = ["group_general@teamforce.ru", "group_buh@teamforce.ru", "group_contracts@teamforce.ru",
                           "group_treasury@teamforce.ru", "group_kdp@teamforce.ru", "group_coordination@teamforce.ru",
                           "group_development@teamforce.ru", "group_recruitment@teamforce.ru",
                           "group_resource-management@teamforce.ru", "group_services@teamforce.ru",
                           "group_tech@teamforce.ru",
                           "group_tenders@teamforce.ru", "partnership@teamforce.ru", "team@teamforce.ru",
                           "Другое (Ввести вручную)"]
            cbq_list = ["group_general@teamforce.ru", "group_buh@teamforce.ru", "group_contracts@teamforce.ru",
                        "group_treasury@teamforce.ru", "group_kdp@teamforce.ru", "group_coordination@teamforce.ru",
                        "group_development@teamforce.ru", "group_recruitment@teamforce.ru",
                        "group_resource-management@teamforce.ru", "group_services@teamforce.ru",
                        "group_tech@teamforce.ru",
                        "group_tenders@teamforce.ru", "partnership@teamforce.ru", "team@teamforce.ru", "Другое"]

            button_list_list = list_split(button_list, 5)
            cbq_list_list = list_split(cbq_list, 5)
            pagi_data = create_pagi_data(button_list_list, cbq_list_list)

            legal_entity_kb = create_kb_next(buttons_text=button_list[0:5], callback_data=cbq_list[0:5])
            to_edit = await bot.edit_message_text(f"Основная группа (только для команды):",
                                                  reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
                data["pagi"] = pagi_data
                data["pagi_step"] = 0
            await FSM_newbie_xlsx.step_22.set()

        elif data["state"] == "FSM_newbie_xlsx:step_22":
            async with state.proxy() as data:
                data["Основная группа"] = message.text
            button_list = ["нет", "group_general@teamforce.ru", "group_buh@teamforce.ru",
                           "group_contracts@teamforce.ru",
                           "group_treasury@teamforce.ru", "group_kdp@teamforce.ru", "group_coordination@teamforce.ru",
                           "group_development@teamforce.ru", "group_recruitment@teamforce.ru",
                           "group_resource-management@teamforce.ru", "group_services@teamforce.ru",
                           "group_tech@teamforce.ru",
                           "group_tenders@teamforce.ru", "partnership@teamforce.ru", "team@teamforce.ru",
                           "Другое (Ввести вручную)"]
            cbq_list = ["нет", "group_general@teamforce.ru", "group_buh@teamforce.ru", "group_contracts@teamforce.ru",
                        "group_treasury@teamforce.ru", "group_kdp@teamforce.ru", "group_coordination@teamforce.ru",
                        "group_development@teamforce.ru", "group_recruitment@teamforce.ru",
                        "group_resource-management@teamforce.ru", "group_services@teamforce.ru",
                        "group_tech@teamforce.ru",
                        "group_tenders@teamforce.ru", "partnership@teamforce.ru", "team@teamforce.ru", "Другое"]

            button_list_list = list_split(button_list, 5)
            cbq_list_list = list_split(cbq_list, 5)
            pagi_data = create_pagi_data(button_list_list, cbq_list_list)

            legal_entity_kb = create_kb_next(buttons_text=button_list[0:5], callback_data=cbq_list[0:5])
            to_edit = await bot.edit_message_text(f"Другие группы:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
                data["pagi"] = pagi_data
                data["pagi_step"] = 0
            await FSM_newbie_xlsx.step_23.set()

        elif data["state"] == "FSM_newbie_xlsx:step_23":
            async with state.proxy() as data:
                data["Другие группы"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"Ноутбук:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_24.set()

        elif data["state"] == "FSM_newbie_xlsx:step_24":
            async with state.proxy() as data:
                data["Ноутбук"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"Внешний монитор:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_25.set()

        elif data["state"] == "FSM_newbie_xlsx:step_25":
            async with state.proxy() as data:
                data["Внешний монитор"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"Телефон:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_26.set()

        elif data["state"] == "FSM_newbie_xlsx:step_26":
            async with state.proxy() as data:
                data["Телефон"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"Флэшка:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_27.set()

        elif data["state"] == "FSM_newbie_xlsx:step_27":
            async with state.proxy() as data:
                data["Флэшка"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"Модем:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.step_28.set()

        elif data["state"] == "FSM_newbie_xlsx:step_28":
            async with state.proxy() as data:
                data["Модем"] = message.text
            button_list = ["Да", "Нет", "Другое"]
            cbq_list = ["Да", "Нет", "Другое"]
            legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            to_edit = await bot.edit_message_text(f"Мобильная связь:", reply_markup=legal_entity_kb,
                                                  chat_id=message.from_user.id,
                                                  message_id=data["to_edit"].message_id)
            async with state.proxy() as data:
                data["to_edit"] = to_edit
            await FSM_newbie_xlsx.commit_data.set()

        elif data["state"] == "FSM_newbie_xlsx:commit_data":
            async with state.proxy() as data:
                data["Мобильная связь"] = message.text
                text = "Давай проверим что получилось:\n\n" \
                       f'Фамилия: <code>{data["surname"]}</code>\n' \
                       f'Фамилия (англ.) <code>{data["surname_eng"]}</code>\n' \
                       f'Имя <code>{data["name"]}</code>\n' \
                       f'Отчество <code>{data["patronim"]}</code>\n' \
                       f'День рождения <code>{data["date_of_birth"]}</code>\n' \
                       f'Телефон <code>{data["phone"]}</code>\n' \
                       f'E-mail <code>{data["email"]}</code>\n' \
                       f'ЮЛ <code>{data["legal_entity"]}</code>\n' \
                       f'Тип сотрудника <code>{data["emp_type"]}</code>\n' \
                       f'Формат сотрудничества <code>{data["type_of_cooperation"]}</code>\n' \
                       f'Офис <code>{data["office"]}</code>\n' \
                       f'Дата выхода <code>{data["first_work_day"]}</code>\n' \
                       f'Центр расходов <code>{data["expense_center"]}</code>\n' \
                       f'Руководитель <code>{data["superviser"]}</code>\n' \
                       f'Бизнес-роль <code>{data["business_role"]}</code>\n' \
                       f'Удаленный доступ <code>{data["Удаленный доступ"]}</code>\n\n' \
                       f'<b>Информационные ресурсы</b>\n' \
                       f'БУХ <code>{data["БУХ"]}</code>\n' \
                       f'ЗУП <code>{data["ЗУП"]}</code>\n' \
                       f'ДОК <code>{data["ДОК"]}</code>\n' \
                       f'СБИС <code>{data["СБИС"]}</code>\n\n' \
                       f'<b>Файловые ресурсы</b>\n' \
                       f'Public <code>{data["Public"]}</code>\n' \
                       f'Findoc <code>{data["Findoc"]}</code>\n' \
                       f'КДП <code>{data["КДП"]}</code>\n' \
                       f'FindocBK <code>{data["FindocBK"]}</code>\n\n' \
                       f'Внешние сервисы\n' \
                       f'Контур Фокус <code>{data["Контур Фокус"]}</code>\n' \
                       f'Бикотендер <code>{data["Бикотендер"]}</code>\n' \
                       f'Консультант+ <code>{data["Консультант+"]}</code>\n' \
                       f'Доступ 1С <code>{data["Доступ 1С"]}</code>\n' \
                       f'Домен почты <code>{data["Домен почты"]}</code>\n' \
                       f'Дополнительный домен почты <code>{data["Дополнительный домен почты"]}</code>\n' \
                       f'Основная группа (только для команды) <code>{data["Основная группа"]}</code>\n' \
                       f'Другие группы <code>{data["Другие группы"]}</code>\n\n' \
                       f'<b>Оборудование</b>\n' \
                       f'Ноутбук <code>{data["Ноутбук"]}</code>\n' \
                       f'Внешний монитор <code>{data["Внешний монитор"]}</code>\n' \
                       f'Телефон <code>{data["Телефон"]}</code>\n' \
                       f'Флэшка <code>{data["Флэшка"]}</code>\n' \
                       f'Модем <code>{data["Модем"]}</code>\n\n' \
                       f'<b>Услуги</b>\n' \
                       f'Мобильная связь <code>{message.text}</code>'
            button_list = ["Отправляем", "Редактируем", "Получить xlsx фаил"]
            cbq_list = ["Отправляем", "Редактируем", "Получить xlsx фаил"]
            temp_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
            await bot.edit_message_text(text, message.from_user.id, data["to_edit"].message_id,
                                        reply_markup=temp_kb,
                                        parse_mode=types.ParseMode.HTML)
            await FSM_newbie_xlsx.finish.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.finish)
async def finish(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        create_newbie_xlsx(
            filepath="new_employer.xlsx",
            surname=data["surname"],
            surname_eng=data["surname_eng"],
            name=data["name"],
            patronim=data["patronim"],
            date_of_birth=data["date_of_birth"],
            phone=data["phone"],
            email=data["email"],
            superviser=data["superviser"],
            legal_entity=data["legal_entity"],
            emp_type=data["emp_type"],
            type_of_cooperation=data["type_of_cooperation"],
            office=data["office"],
            first_work_day=data["first_work_day"],
            expense_center=data["expense_center"],
            business_role=data["business_role"],
            b21=data["Удаленный доступ"],
            b24=data["БУХ"],
            b25=data["ЗУП"],
            b26=data["ДОК"],
            b27=data["СБИС"],
            b30=data["Public"],
            b31=data["Findoc"],
            b32=data["КДП"],
            b33=data["FindocBK"],
            b35=data["Контур Фокус"],
            b36=data["Бикотендер"],
            b37=data["Консультант+"],
            b39=data["Доступ 1С"],
            b41=data["Домен почты"],
            b42=data["Дополнительный домен почты"],
            b44=data["Основная группа"],
            b45=data["Другие группы"],
            b48=data["Ноутбук"],
            b49=data["Внешний монитор"],
            b50=data["Телефон"],
            b51=data["Флэшка"],
            b52=data["Модем"],
            b55=data["Мобильная связь"],
        )
    if callback_query.data == "Получить xlsx фаил":
        with open("new_employer.xlsx", "rb") as file:
            await bot.send_document(chat_id=callback_query.from_user.id, document=file)
        button_list = ["Отправляем", "Редактируем", "Выйти"]
        cbq_list = ["Отправляем", "Редактируем", "Выйти"]
        temp_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
        await callback_query.message.edit_reply_markup(reply_markup=temp_kb)
    elif callback_query.data == "Отправляем":
        await callback_query.message.edit_reply_markup(reply_markup=None)
        msg = await callback_query.message.answer("Отправляю xlsx ... (в работе)")
        async with state.proxy() as data:
            send_email = asyncio.create_task(send_create_corp_email(
                name=data["name"],
                surname=data["surname"],
                patronim=data["patronim"],
                date_of_birth=data["date_of_birth"],
                legal_entity=data["legal_entity"],
                first_work_day="today",  # todo забирать из основной анкеты
                superviser=data["superviser"],
                job_title="Название должности",  # todo забирать из основной анкеты
                mail_domain=data["Домен почты"],
                xlsx_path="new_employer.xlsx"
            ))
            if send_email:
                await bot.edit_message_text(text="Сообщение отправлено",
                                            chat_id=callback_query.from_user.id,
                                            message_id=msg.message_id)
            else:
                await bot.edit_message_text(text="Сообщение отправлено",
                                            chat_id=callback_query.from_user.id,
                                            message_id=msg.message_id)
        await state.finish()
    elif callback_query.data == "Редактируем":
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.message.answer("Тут будет клавиатура для редактирования отдельных параметров")
        await state.finish()
    elif callback_query.data == "Выйти":
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.message.answer("Совершен выход из анкеты, данные удалены")
        await state.finish()
    await delete_temp_file("new_employer.xlsx")


def register_handlers_create_xlsx(dp: Dispatcher):
    pass
