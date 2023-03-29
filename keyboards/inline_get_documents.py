from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""
Клавиатуры для вывода кнопки для скачивания документов
"""

get_annual_leave_button = InlineKeyboardButton(text="Скачать заявление на ежегодный отпуск",
                                               callback_data="get annual_leave_application")
get_business_trip_regulation_button = InlineKeyboardButton(text="Скачать положение о служебных командировках",
                                                           callback_data="get business_trip_regulation")
get_official_memo_button = InlineKeyboardButton(text="Скачать служебную записку", callback_data="get official_memo")
get_application_for_funds_button = InlineKeyboardButton(text="Скачать заявление на выдачу подотчетных средств",
                                                        callback_data="get application_for_funds")
get_teamforce_presentation_button = InlineKeyboardButton(text="Скачать презентацию Teamforce",
                                                         callback_data="get teamforce_presentation")
get_vacation_at_own_button = InlineKeyboardButton(text="Скачать заявление на отпуск за свой счет",
                                                  callback_data="get vacation_at_own")
start_bt_form_sending = InlineKeyboardButton(text="Отправить заявление на командировку",
                                             callback_data="start_bt_form")


get_annual_leave = InlineKeyboardMarkup(row_width=1).add(get_annual_leave_button)
get_business_trip_docs_keyboard = InlineKeyboardMarkup(row_width=1).add(get_business_trip_regulation_button,
                                                                        get_official_memo_button,
                                                                        get_application_for_funds_button,
                                                                        start_bt_form_sending)
get_teamforce_presentation_keyboard = InlineKeyboardMarkup(row_width=1).add(get_teamforce_presentation_button)
get_get_vacation_at_own_keyboard = InlineKeyboardMarkup(row_width=1).add(get_vacation_at_own_button)
