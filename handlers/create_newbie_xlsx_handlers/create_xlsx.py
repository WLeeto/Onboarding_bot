from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from States.states import FSM_newbie_xlsx
from create_bot import dp, bot, db
from dicts.messages import expense_center_xlsx_dict, business_role_xlsx_dict
from func.all_func import is_breakes, delete_temp_file
from func.create_xlsx import create_newbie_xlsx
from keyboards.inline_xlsx_newbie_form import create_kb


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
                   "ООО «ТАТМобайлИнформ СиДиСи»", 'ООО "Репола"', 'ООО "Сириус"', 'ООО "Кайрос"', 'ООО "Бивень"']
    cbq_list = ["ООО «СмартСтаффинг»", "ООО «ТИМ ФОРС»", "ООО «ТИМ ФОРС Сервис»", "ООО «ТИМ ФОРС Менеджмент»",
                "ООО «ТАТМобайлИнформ СиДиСи»", 'ООО "Репола"', 'ООО "Сириус"', 'ООО "Кайрос"', 'ООО "Бивень"']
    legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
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


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_1)
async def employer_type(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["legal_entity"] = callback_query.data
    await callback_query.answer()
    button_list = ["Команда", "Проекты"]
    cbq_list = ["Команда", "Проекты"]
    legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
    to_edit = await bot.edit_message_text(f"Тип сотрудника:", reply_markup=legal_entity_kb,
                                          chat_id=callback_query.from_user.id,
                                          message_id=data["to_edit"].message_id)
    async with state.proxy() as data:
        data["to_edit"] = to_edit
    await FSM_newbie_xlsx.step_2.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_2)
async def employer_type2(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["emp_type"] = callback_query.data
    await callback_query.answer()
    button_list = ["Штат", "Внешний"]
    cbq_list = ["Штат", "Внешний"]
    legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
    to_edit = await bot.edit_message_text(f"Формат сотрудничества:", reply_markup=legal_entity_kb,
                                          chat_id=callback_query.from_user.id,
                                          message_id=data["to_edit"].message_id)
    async with state.proxy() as data:
        data["to_edit"] = to_edit
    await FSM_newbie_xlsx.step_3.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_3)
async def employer_type3(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["type_of_cooperation"] = callback_query.data
    await callback_query.answer()
    button_list = ["Сколково", "Удаленка", "Гибрид"]
    cbq_list = ["Сколково", "Удаленка", "Гибрид"]
    legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list)
    to_edit = await bot.edit_message_text(f"Офис:", reply_markup=legal_entity_kb,
                                          chat_id=callback_query.from_user.id,
                                          message_id=data["to_edit"].message_id)
    async with state.proxy() as data:
        data["to_edit"] = to_edit
    await FSM_newbie_xlsx.step_4.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_4)
async def employer_type4(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["office"] = callback_query.data
    await callback_query.answer()
    button_list = ["/Блок Проекты", "/Блок Проекты/Группа договорной работы", "/Блок Проекты/Группа координаторов",
                   "/Блок Проекты/Тендерная группа", "/Блок Развитие", "/Блок Ресурсы", "/Блок Ресурсы/Отдел КДП",
                   "/Блок Ресурсы/Отдел рекрутмента", "/Блок Ресурсы/Группа ресурсного менджмента", "/Блок Сервисы",
                   "/Блок Технологии", "/Блок Финансы/Бухгалтерия", "/Блок Финансы/Казначейство"]
    cbq_list = ["1", "2", "3",
                "4", "5", "6", "7",
                "8", "9", "10",
                "11", "12", "13"]
    legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list, row_width=2)
    to_edit = await bot.edit_message_text(f"Центр расходов:", reply_markup=legal_entity_kb,
                                          chat_id=callback_query.from_user.id,
                                          message_id=data["to_edit"].message_id)
    async with state.proxy() as data:
        data["to_edit"] = to_edit
    await FSM_newbie_xlsx.step_5.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.step_5)
async def employer_type5(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["expense_center"] = expense_center_xlsx_dict[f"{callback_query.data}"]
    await callback_query.answer()
    button_list = ["Основатель", "Операционный директор", "Директор программы", "Директор блока", "Лидер группы",
                   "Руководитель проектов", "Аккаунт-менеджер", "Специалист по договорной работе",
                   "Тендерный специалист", "Координатор проектов", "Партнерский менеджер", "Специалист КДП",
                   "Рекрутер", "Ресурсный менеджер", "Менеджер", "Руководитель ИТ-службы", "Юрист", "Менеджер продукта",
                   "Разработчик B2BCloud", "Бухгалтер по основной деятельности", "Бухгалтер",
                   "Бухгалтер по вспомогательной деятельности", "Бухгалтер по расчету заработной платы",
                   "Главный бухгалтер", "Бухгалтер-операционист", "Финансовый менджер", "Стажер", "Разработчик PHP",
                   "Разработчик JS", "Тестировщик", "Python разработчик", "Ассистент отдела развития"]
    cbq_list = ["1", "2", "3", "4", "5",
                "6", "7", "8",
                "9", "10", "11", "12",
                "13", "14", "15", "16", "17", "18",
                "19", "20", "21",
                "22", "23",
                "24", "25", "26", "27", "28",
                "29", "30", "31", "32"]
    legal_entity_kb = create_kb(buttons_text=button_list, callback_data=cbq_list, row_width=4)
    to_edit = await bot.edit_message_text(f"Бизнес-роль:", reply_markup=legal_entity_kb,
                                          chat_id=callback_query.from_user.id,
                                          message_id=data["to_edit"].message_id)
    async with state.proxy() as data:
        data["to_edit"] = to_edit
    await FSM_newbie_xlsx.finish.set()


@dp.callback_query_handler(state=FSM_newbie_xlsx.finish)
async def finish(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        create_newbie_xlsx(
            filepath="test.xlsx",
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
            business_role=business_role_xlsx_dict[f"{callback_query.data}"],
        )
    with open("test.xlsx", "rb") as file:
        await bot.send_document(chat_id=callback_query.from_user.id, document=file)
    await delete_temp_file("test.xlsx")


def register_handlers_create_xlsx(dp: Dispatcher):
    pass
