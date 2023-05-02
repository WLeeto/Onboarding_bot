import openpyxl
from openpyxl.styles import Font


def create_newbie_xlsx(filepath, **kwargs) -> bool:
    """
    Создает фаил для отправки ИТ-директору
    :param filepath: Путь до фаила
    :param kwargs:
    :return:
    """
    wb = openpyxl.Workbook()
    work_sheet = wb.create_sheet("Прием", 0)

    work_sheet.column_dimensions['A'].width = 30
    work_sheet.column_dimensions['B'].width = 30

    work_sheet["A2"] = "Фамилия"
    work_sheet["A3"] = "Фамилия (англ.)"
    work_sheet["A4"] = "Имя"
    work_sheet["A5"] = "Отчество"
    work_sheet["A6"] = "День рождения"
    work_sheet["A8"] = "Телефон"
    work_sheet["A9"] = "E-mail"
    work_sheet["A11"] = "ЮЛ"
    work_sheet["A12"] = "Тип сотрудника"
    work_sheet["A13"] = "Формат сотрудничества"
    work_sheet["A14"] = "Офис"
    work_sheet["A15"] = "Дата выхода"
    work_sheet["A17"] = "Центр расходов"
    work_sheet["A18"] = "Руководитель"
    work_sheet["A19"] = "Бизнес-роль"
    work_sheet["A21"] = "Удаленный доступ"
    work_sheet["A23"] = "Информационные ресурсы"
    work_sheet["A24"] = "БУХ"
    work_sheet["A25"] = "ЗУП"
    work_sheet["A26"] = "ДОК"
    work_sheet["A27"] = "СБИС"
    work_sheet["A29"] = "Файловые ресурсы"
    work_sheet["A30"] = "Public"
    work_sheet["A31"] = "Findoc"
    work_sheet["A32"] = "КДП"
    work_sheet["A33"] = "FindocBK"
    work_sheet["A34"] = "Внешние сервисы"
    work_sheet["A35"] = "Контур Фокус"
    work_sheet["A36"] = "Бикотендер"
    work_sheet["A37"] = "Консультант+"
    work_sheet["A39"] = "Доступ 1С"
    work_sheet["A41"] = "Домен почты"
    work_sheet["A42"] = "Дополнительный домен почты"
    work_sheet["A44"] = "Основная группа (только для команды)"
    work_sheet["A45"] = "Другие группы"
    work_sheet["A47"] = "Оборудование"
    work_sheet["A48"] = "Ноутбук"
    work_sheet["A49"] = "Внешний монитор"
    work_sheet["A50"] = "Телефон"
    work_sheet["A51"] = "Флэшка"
    work_sheet["A52"] = "Модем"
    work_sheet["A54"] = "Услуги"
    work_sheet["A55"] = "Мобильная связь"

    work_sheet["B2"] = kwargs.get("surname")
    work_sheet["B3"] = kwargs.get("surname_eng")
    work_sheet["B4"] = kwargs.get("name")
    work_sheet["B5"] = kwargs.get("patronim")
    work_sheet["B6"] = kwargs.get("date_of_birth")
    work_sheet["B8"] = kwargs.get("phone")
    work_sheet["B9"] = kwargs.get("email")
    work_sheet["B11"] = kwargs.get("legal_entity")
    work_sheet["B12"] = kwargs.get("emp_type")
    work_sheet["B13"] = kwargs.get("type_of_cooperation")
    work_sheet["B14"] = kwargs.get("office")
    work_sheet["B15"] = kwargs.get("first_work_day")
    work_sheet["B17"] = kwargs.get("expense_center")
    work_sheet["B18"] = kwargs.get("superviser")
    work_sheet["B19"] = kwargs.get("business_role")
    work_sheet["B21"] = kwargs.get("b21")

    work_sheet["B24"] = kwargs.get("b24")
    work_sheet["B25"] = kwargs.get("b25")
    work_sheet["B26"] = kwargs.get("b26")
    work_sheet["B27"] = kwargs.get("b27")

    work_sheet["B30"] = kwargs.get("b30")
    work_sheet["B31"] = kwargs.get("b31")
    work_sheet["B32"] = kwargs.get("b32")
    work_sheet["B33"] = kwargs.get("b33")

    work_sheet["B35"] = kwargs.get("b35")
    work_sheet["B36"] = kwargs.get("b36")
    work_sheet["B37"] = kwargs.get("b37")
    work_sheet["B39"] = kwargs.get("b39")
    work_sheet["B41"] = kwargs.get("b41")
    work_sheet["B42"] = kwargs.get("b42")
    work_sheet["B44"] = kwargs.get("b44")
    work_sheet["B45"] = kwargs.get("b45")

    work_sheet["B48"] = kwargs.get("b48")
    work_sheet["B49"] = kwargs.get("b49")
    work_sheet["B50"] = kwargs.get("b50")
    work_sheet["B51"] = kwargs.get("b51")
    work_sheet["B52"] = kwargs.get("b52")

    work_sheet["B55"] = kwargs.get("b55")

    work_sheet_a23 = work_sheet["A23"]
    work_sheet_a23.font = Font(bold=True)
    work_sheet_a29 = work_sheet["A29"]
    work_sheet_a29.font = Font(bold=True)
    work_sheet_a34 = work_sheet["A34"]
    work_sheet_a34.font = Font(bold=True)
    work_sheet_a47 = work_sheet["A47"]
    work_sheet_a47.font = Font(bold=True)
    work_sheet_a54 = work_sheet["A54"]
    work_sheet_a54.font = Font(bold=True)

    wb.save(filepath)
