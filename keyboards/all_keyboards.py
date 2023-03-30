from keyboards.inline_find import search_way
from keyboards.inline_get_documents import get_annual_leave, get_get_vacation_at_own_keyboard, \
    get_teamforce_presentation_keyboard, get_business_trip_docs_keyboard
from keyboards.inline_initiate_vacation import start_sending_vacation_email_keyboard
from keyboards.inline_contacts import start_search_by_phone
from keyboards.inline_finance import finance_staff_choose_kb
from keyboards.inline_sick_leave import sick_leave_kb

"""
Словарь со всеми клавиатурами для вызова из БД
"""

all_keyboards = {
    "get_annual_leave": get_annual_leave,
    "search_way": search_way,
    "vacation_at_own": get_get_vacation_at_own_keyboard,
    "start_sending_vacation_email": start_sending_vacation_email_keyboard,
    "start_search_by_phone": start_search_by_phone,
    "get_teamforce_presentation_keyboard": get_teamforce_presentation_keyboard,
    "get_business_trip_docs_keyboard": get_business_trip_docs_keyboard,
    "finance_staff_choose_kb": finance_staff_choose_kb,
    "sick_leave_kb": sick_leave_kb,
}