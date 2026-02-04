from aiogram import types
from loader import dp, db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from keyboards.inline.admin_tugma import ogit_keyboard


@dp.callback_query_handler(lambda call: "ogit:" in call.data)
async def barcha_dorilar(call: types.CallbackQuery):
    _, ogit = call.data.split(":")
    ogit = ogit.replace('📂 ', '')
    text, tugma = await dorilar_hammasi(ogit=ogit)
    await call.message.answer(text=text, reply_markup=tugma)

@dp.message_handler(text="🛒 O'g'itlar Do'koni")
async def add_medicine_name(message: types.Message):
    await message.answer("og'it turini tanlang?", reply_markup=ogit_keyboard())

@dp.callback_query_handler(lambda call: "page1:" in call.data)
async def dorilar(call: types.CallbackQuery):
    await call.message.answer(text=text, reply_markup=tugma)
    try:
        _, page, ogit = call.data.split(":")
        if int(page) > 0:
            text, tugma = await dorilar_hammasi(page, ogit=ogit)
            if text:
                await call.message.delete()
                await call.message.answer(text=f"📋 {text}", reply_markup=tugma)
            else:
                await call.answer("dorilar topilmadi")
        else:
            await call.answer("dorilar topilmadi")
    except:
        await call.answer("dorilar topilmadi")


@dp.callback_query_handler(lambda call: "dori:" in call.data)
async def dorilar_buyutma(call: types.CallbackQuery):
    try:
        _, dori_id = call.data.split(":")
        user_id = (db.select_users(call.from_user.id))[0]
        db.add_order(user_id=user_id, medicine_id=dori_id)
        await call.answer("Buyurtmangiz saqlandi. Tez orada siz bilan bog'lanamiz")
    except Exception as e:
        print(e)
    


async def dorilar_hammasi(ogit, page=1):
    try:
        uzunlik = (db.dori_count_user(crop=ogit))[0]
        if uzunlik+10 - page*10 >0:
            dorilar = db.select_all_dori_user(crop=ogit, page=page)
        else:
            dorilar = None
        keyboard = InlineKeyboardMarkup(row_width=3)
        if dorilar:
            keyboard = InlineKeyboardMarkup(row_width=5)
            s = page*10-10+1
            text = f"dorilar ro'yhati {s}-{page*10}: {uzunlik}. \n buyurtma qilish uchun maxsulot raqamini bosing !"
            for son, dori in enumerate(dorilar, start=1):
                text += '\n' + f"{son}. id: {dori[0]}"
                text += f"\n name: {dori[1]}"
                text += f"\n crop: {dori[2]}"
                text += f"\n description: {dori[3]}"
                text += f"\n price: {dori[4]}"
                text += f"\n _________________________\n"
                keyboard.insert(InlineKeyboardButton(text=f"{son}", callback_data=f"dori:{dori[0]}"))
            keyboard.row(
                InlineKeyboardButton("◀", callback_data=f"page1:{page-1}:{ogit}"),
                InlineKeyboardButton("▶", callback_data=f"page1:{page+1}:{ogit}"),
            )
            return text, keyboard
        else:
            return "og'itlar mavjud emas", keyboard
    except Exception as e:
        return 
