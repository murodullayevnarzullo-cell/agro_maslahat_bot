from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Admin asosiy menyu
def admin_main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="Savollarga javob", callback_data="admin_questions"),
        InlineKeyboardButton(text="Dorilar boshqaruvi", callback_data="admin_medicines"),
        InlineKeyboardButton(text="Buyurtmalarni kuzatish", callback_data="admin_orders"),
        InlineKeyboardButton(text="Adminlar ro'yxati", callback_data="admin_list")
    )
    return keyboard

# Dorilar boshqaruvi menyusi
def admin_medicines_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="Dori qo'shish", callback_data="medicine_add"),
        InlineKeyboardButton(text="Dori tahrirlash", callback_data="medicine_edit"),
        InlineKeyboardButton(text="Dori o'chirish", callback_data="medicine_delete"),
    )
    return keyboard

# Savollarga javob berish tugmalari
def admin_questions_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="Yangi savollar", callback_data="questions_new"),
        InlineKeyboardButton(text="Barchasi", callback_data="questions_all"),
        InlineKeyboardButton(text="Orqaga", callback_data="admin_back")
    )
    return keyboard

# Buyurtmalarni boshqarish
def admin_orders_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="Yangi buyurtmalar", callback_data="orders_new"),
        InlineKeyboardButton(text="Barchasi", callback_data="orders_all"),
        InlineKeyboardButton(text="Orqaga", callback_data="admin_back")
    )
    return keyboard

# Adminlar ro'yxati
def admin_list_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="Admin qo'shish", callback_data="admin_add"),
        InlineKeyboardButton(text="Admin o'chirish", callback_data="admin_delete"),
        InlineKeyboardButton(text="Orqaga", callback_data="admin_back")
    )
    return keyboard

def ogit_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)

    districts = [
        "📂 Azotli o'g'itlar",
        " 📂 Fosforli o'g'itlar",
        "📂 Kaliyli o'g'itlar",
        "📂 Kompleks (NPK) o'g'itlar"
    ]

    for d in districts:
        keyboard.insert(
            InlineKeyboardButton(
                text=d,
                callback_data=f"ogit:{d}"
            )
        )

    return keyboard