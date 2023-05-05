from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

January = InlineKeyboardButton(text="Январь", callback_data="bday January")
February = InlineKeyboardButton(text="Февраль", callback_data="bday February")
March = InlineKeyboardButton(text="Март", callback_data="bday March")
April = InlineKeyboardButton(text="Апрель", callback_data="bday April")
May = InlineKeyboardButton(text="Май", callback_data="bday May")
June = InlineKeyboardButton(text="Июнь", callback_data="bday June")
July = InlineKeyboardButton(text="Июль", callback_data="bday July")
August = InlineKeyboardButton(text="Август", callback_data="bday August")
September = InlineKeyboardButton(text="Сентябрь", callback_data="bday September")
October = InlineKeyboardButton(text="Октябрь", callback_data="bday October")
November = InlineKeyboardButton(text="Ноябрь", callback_data="bday November")
December = InlineKeyboardButton(text="Декабрь", callback_data="bday December")
bday_kb = InlineKeyboardMarkup(row_width=3)\
    .add(January, February, March).add(April, May, June).add(July, August, September).add(October, November, December)

