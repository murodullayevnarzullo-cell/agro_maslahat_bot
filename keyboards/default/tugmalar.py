from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def phone_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("📞 Raqamni yuborish", request_contact=True)
    )
    return keyboard

def user_main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        KeyboardButton(text="🧑‍🌾 AI maslahati"),
        KeyboardButton(text="🧑‍🌾 Mutaxassis maslahati"),
        KeyboardButton(text="📦 Buyurtmalarim"),
        KeyboardButton(text="🛒 O'g'itlar Do'koni"),
        KeyboardButton(text="📞 Aloqa")
    )
    return keyboard

def admin_main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        KeyboardButton(text="Savollarga javob"),
        KeyboardButton(text="🛒 O'g'itlar boshqaruvi"),
        KeyboardButton(text="Buyurtmalarni kuzatish"),
        KeyboardButton(text="Adminlar ro'yxati"),
        KeyboardButton(text="📞 Aloqa")
    )
    return keyboard