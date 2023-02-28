from keyboards.inline_find import search_way
from keyboards.inline_get_documents import get_annual_leave

"""
Словарь со всеми клавиатурами для вызова из БД
"""

all_keyboards = {
    "get_annual_leave": get_annual_leave,
    "search_way": search_way,
}