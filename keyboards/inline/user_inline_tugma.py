from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def district_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)

    districts = [
        "Andijon shahri",
        "Andijon tumani",
        "Asaka",
        "Baliqchi",
        "Bo‘ston",
        "Buloqboshi",
        "Izboskan",
        "Jalakuduk",
        "Marhamat",
        "Oltinko‘l",
        "Paxtaobod",
        "Qo‘rg‘ontepa",
        "Shahrixon",
        "Ulug‘nor",
        "Xo‘jaobod"
    ]

    for d in districts:
        keyboard.insert(
            InlineKeyboardButton(
                text=d,
                callback_data=f"district:{d}"
            )
        )

    return keyboard




