from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline_get_documents import get_annual_leave_button, get_vacation_at_own_button

"""
Клавиатуры для отпусков
"""

start_sending_vacation_email_button = InlineKeyboardButton(text="Подать заявку на отпуск",
                                                           callback_data="initiate vaсation")
yes_button = InlineKeyboardButton(text="Да", callback_data="answer yes")
no_button = InlineKeyboardButton(text="Нет", callback_data="answer no")
hr_contacts = InlineKeyboardButton(text="Получить контакты отдела кадров", callback_data="hr_contacts")


start_sending_vacation_email_keyboard = InlineKeyboardMarkup(row_width=1).add(get_annual_leave_button,
                                                                              start_sending_vacation_email_button)
start_sending_vacation_email_keyboard_o = InlineKeyboardMarkup(row_width=1).add(get_vacation_at_own_button,
                                                                                start_sending_vacation_email_button,
                                                                                hr_contacts)

yes_no_keyboard = InlineKeyboardMarkup(row_width=1).add(yes_button, no_button)


more_than_two_weeks_button = InlineKeyboardButton(text="Отпуск за 2 недели", callback_data="vacation more")
less_than_two_weeks_button = InlineKeyboardButton(text="Отпуск меньше чем за 2 недели", callback_data="vacation less")
holiday_pay_button = InlineKeyboardButton(text="Отпускные", callback_data="vacation pay_info")

vacation_keyboard = InlineKeyboardMarkup(row_width=1).add(more_than_two_weeks_button, less_than_two_weeks_button,
                                                          holiday_pay_button)