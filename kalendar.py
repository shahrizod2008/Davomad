import calendar
from datetime import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_calendar(year: int=None, Month: int=None):
    if year is None:
        year=datetime.now().year
    if Month is None:
        year=datetime.now().month

    cal=calendar.monthcalendar(year, Month)

    markup=InlineKeyboardMarkup(inline_keyboard=[])

    days_of_week=["Mo", "Tu", "We", "Th", "Sa", "Su"]

    markup.inline_keyboard.append([InlineKeyboardButton(text=day, callback_data="ignore") for day in days_of_week])


    for week in cal:
        row=[]
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton( text= " ", callback_data="ignore"))
            else:
                row.append (InlineKeyboardButton(text= str(day), callback_data= f"day_{day}_{Month}_{year}"))

            markup.inline_keyboard.append(row)

    prew_button=InlineKeyboardButton(text= "<", callback_data= f" prew_month_{year}_{Month}")
    next_button=InlineKeyboardButton(text= ">", callback_data= f" next_month_{year}_{Month}")

    month_year_button=InlineKeyboardButton(text= f"{calendar.month_name[Month]} {year}", callback_data= "ignore")


    markup.inline_keyboard.append([prew_button, month_year_button, next_button])

    return markup