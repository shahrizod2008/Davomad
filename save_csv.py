import os, csv
import aiofiles
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime


# CSV fayliga yozish funksiyasi
def save_to_csv(data):
    telegram_id = data[1]  # Ma'lumotlar ichidan Telegram ID ni olish

    # CSV fayli mavjudligini tekshiramiz
    file_exists = os.path.isfile("users.csv")

    # Faylni o'qish rejimida ochib, ID ni tekshiramiz
    if file_exists:
        with open("users.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Sarlavhani o'tkazib yuboramiz

            # Telegram ID faylda bor yoki yo'qligini tekshiramiz
            for row in reader:
                if row[1] == str(telegram_id):  # Telegram ID ni tekshirish
                    return  # Foydalanuvchi topildi, yozmaymiz

    # Faylga yozish (agar foydalanuvchi topilmagan bo'lsa)
    with open("users.csv", mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)

        # Agar fayl avval yaratilmagan bo'lsa, sarlavha yozish
        if not file_exists:
            writer.writerow(["Name", "Telegram ID", "Group ID"])

        # Foydalanuvchi ma'lumotlarini yozish
        writer.writerow(data)


# CSV fayldan o'qib, har bir foydalanuvchi uchun tugma yaratish funksiyasi
def get_user_buttons():
    buttons = []  # InlineKeyboardMarkup obyektini yaratamiz

    if os.path.isfile("users.csv"):
        with open("users.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Sarlavhani o'tkazib yuborish

            for row in reader:
                user_name, telegram_id, group_id = row

                # Har bir foydalanuvchi uchun tugma yaratish
                button = InlineKeyboardButton(text=user_name, callback_data=f"user_{telegram_id}")
                print(button)
                buttons.append(button)  # Tugmani qo'shamiz
    buttons = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return buttons


async def day_attendance(data):
    telegram_id=data[1]

    today=datetime.today().date()

    file_exists=os.path.isfile(f"{today}.csv")

    if file_exists:
        async with aiofiles.open( f"{today}.csv", mode="r",encoding="utf-8") as file:
            contents =await file.read()
            reader=csv.reader(contents.splitlines())
            next(reader)


            for row in reader:
                if len(row) > 1 and row[1].strip() == str(telegram_id):
                    return False
                
    async  with aiofiles.open(f"{today}.csv", mode="a", newline="", encoding="utf-8") as file:
        if not file_exists:
            await file.write("Name, Telegram id, Mavjudlik\n")

        await file.write(f"{data[0]}, {data[1]}, {data[2]}\n")