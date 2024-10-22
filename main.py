import csv
import logging
import asyncio
import os

import aiofiles
from aiogram import Bot, Dispatcher, F
from aiogram. types import Message, CallbackQuery
from aiogram. filters import Command

from button import menu_buttons
from kalendar import create_calendar
from save_csv import save_to_csv, get_user_buttons, day_attendance

API_TOKEN = "7661542067:AAHGh2mX2twGhPSKghCXB1TP_L0bE1HzjM0"


# Loglar uchun sozlash
logging.basicConfig(level=logging. INFO)

# Bot ob'ektini yaratamiz
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def send_file(chat_id, filename):
    if os.path.isfile(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read() # Fayl mazmunini o'qish

            # Agar fayl mazmuni juda katta bo'lsa, uni gismlarga bo'lib yuborish mumkin
            max_message_length = 4096 # Telegramdagi maksimal xabar uzunligi
            for i in range(0, len(content), max_message_length):
                await bot. send_message(chat_id, content[i:i + max_message_length])
    else:
        await bot.send_message(chat_id, "Fayl topilmadi. ")

@dp.message(Command("start"))
async def send_welcome(message: Message):
    user_name = message. from_user. full_name
    telegram_id = message.from_user.id
    group_id = message.chat.id

    # Foydalanuvchi malumotlarini yozish
    save_to_csv([user_name, telegram_id, group_id])

    await message.reply (f"Salom {user_name}! Sizning ma'lumotlaringiz saqlandi.", reply_markup=menu_buttons)


# /help komandasi uchun handler
@dp.message(Command("help"))
async def send_help(message: Message):
    await message.reply ("Yordam menyusi!")


@dp.callback_query(lambda c: c.data and c.data.startswith('day_'))
async def process_day_selection(callback_query: CallbackQuery):
    # Tanlangan kun va oy ma'lumotlarini olish
    _, day, month, year = callback_query.data. split('_')
    selected_date = f"{year}-{month}-{day}" # YYYY-MM-DD formatida
    filename = f"{selected_date}.csv" # Kuningizga mos fayl nomi

    try:
        if callback_query. from_user.id == 104745314:
            await send_file(callback_query.from_user.id, filename)
            await bot. answer_callback_query(callback_query.id, f"Siz {selected_date}-kunni tanladingiz!")
        else:
            print("tel")
            await bot. answer_callback_query(callback_query.id, f"Kalendar orgali faqat admin ko'ra oladi! !! ",show_alert=True)

    except FileNotFoundError:
        await bot.answer_callback_query(callback_query.id, f"{selected_date} uchun fayl topilmadi!")

@dp.callback_query(lambda c: c.data and c.data.startswith('prev_month_'))
async def process_previous_month(callback_query: CallbackQuery):
    year, month = map(int, callback_query. data. split('_') [2:])
    month -= 1
    if month == 0:
       month = 12
       year -= 1

    # Kalendarni yaratish va uni tahrirlash
    markup = create_calendar(year, month)
    await callback_query.message. edit_reply_markup(reply_markup=markup) # reply_markup parametrini to'g'ri qo'shamiz


@dp.callback_query(lambda c: c.data and c.data.startswith('next_month_'))
async def process_next_month(callback_query: CallbackQuery):
    year, month = map(int, callback_query.data. split('_') [2:])
    month += 1
    if month == 13:
        month = 1
        year += 1

    # Kalendarni yaratish va uni tahrirlash
    markup = create_calendar(year, month)
    await callback_query.message.edit_reply_markup(reply_markup=markup) # reply_markup parametrini to'g'ri go'shamiz

@dp.message(Command('calendar'))
async def send_calendar(message: Message) :
    await message. answer("Kalendardan kunni tanlang:", reply_markup=create_calendar())

@dp.message (F.text == 'davomat' )
async def get_user(message: Message):
    await message. answer("Ismingizni tanlang", reply_markup=get_user_buttons())

@dp.callback_query(lambda c: c.data.startswith("user_"))
async def check_user(callback_query: CallbackQuery, bot: Bot):
    telegram_id = callback_query.data.split("_")[1]
    name = callback_query.from_user.full_name

    try:
        async with aiofiles.open("users.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(await file.readlines())
            next(reader) # Sarlavhani o'tkazib yuboramiz

            # Telegram ID faylda bor yoki yo'gligini tekshiramiz
            user_found = False
            for row in reader:
                if row[1] == str(telegram_id) and row[0] == name: # Telegram ID va ismi tekshirish
                    # print(await day_attendance([name, telegram_id, 'ha']))
                    if await day_attendance([name, telegram_id, 'ha']) is False:
                        print("l")
                        await bot. answer_callback_query(callback_query.id,'Siz bugun uchun davomat topshirdingiz!',show_alert=True)
                    else:
                        await day_attendance([name, telegram_id, 'ha'])
                    user_found = True
                    break # Foydalanuvchi topilganda tsiklni tugatamiz

            if not user_found:
                await bot.answer_callback_query(callback_query.id,'Siz boshqa botdan foydalandingiz!')
    except FileNotFoundError:
        await bot.answer_callback_query(callback_query.id,'Fayl topilmadi! ')

    await bot. answer_callback_query(callback_query.id, "Belgilanganizgiz uchun rahmat !!! ")

# Asinxron botni ishga tushirish funksiyasi
async def main():
    # Dispatcher'ni bot bilan bog'laymiz
    dp.startup.register(start_bot)
    dp.shutdown.register(shutdown_bot)

    await dp.start_polling(bot)

async def start_bot(bot: Bot):
    await bot.send_message(6564564050,"Bot ishga tushdi !! ")

async def shutdown_bot(bot: Bot):
    await bot.send_message(6564564050,"Bot o'chdi !! ")

if __name__ == '__main__':
    asyncio.run(main())