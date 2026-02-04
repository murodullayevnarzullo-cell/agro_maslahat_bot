from aiogram import types
from loader import dp, db
from data.config import ADMINS
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery


@dp.message_handler(text="Buyurtmalarni kuzatish")
async def barcha_dorilar_buyutmalar1(msg: types.Message):
    try:
        if str(msg.from_user.id) not in ADMINS:
            if not db.is_admin(msg.from_user.id):
                await msg.answer("Siz admin emassiz!")
                return
        text, tugma = await buyutmalar_hammasi1()
        await msg.answer(text=text, reply_markup=tugma)
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: "page3:" in call.data)
async def dorilar_buyutmalari1(call: types.CallbackQuery):
    await call.message.answer(text=text, reply_markup=tugma)
    try:
        _, page = call.data.split(":")
        if int(page) > 0:
            text, tugma = await buyutmalar_hammasi1(page=page)
            if text:
                await call.message.delete()
                await call.message.answer(text=f"📋 {text}", reply_markup=tugma)
            else:
                await call.answer("dorilar topilmadi")
        else:
            await call.answer("dorilar topilmadi")
    except:
        await call.answer("dorilar topilmadi")


@dp.callback_query_handler(lambda call: "order1:" in call.data)
async def dorilar_buyutma_ochirish1(call: types.CallbackQuery):
    try:
        _, dori_id = call.data.split(":")
        print(dori_id)
        db.delete_order(id=dori_id)
        await call.answer("Buyurtmangiz bekor qilindi !")
        await call.message.ed()
        text, tugma = await buyutmalar_hammasi1(page=1)
        await call.message.delete()
        if text:
            await call.message.answer(text=f"📋 {text}", reply_markup=tugma)
        else:
            await call.answer("Buyurtmalar topilmadi")
    except Exception as e:
        print(e)
    


async def buyutmalar_hammasi1(page=1):
    try:
        uzunlik = (db.orders_all_count())[0]
        if uzunlik+10 - page*10 >0:
            orders = db.select_all_order(page=page)
        else:
            orders = None
        keyboard = InlineKeyboardMarkup(row_width=3)
        if orders:
            keyboard = InlineKeyboardMarkup(row_width=5)
            s = page*10-10+1
            text = f"Buyurtmalar ro'yhati {s}-{page*10}: {uzunlik}. \n Tugallangan buyurtmani ro'yhatdan o'chirish uchun mos raqam tugmanisini bosing !"
            for son, order in enumerate(orders, start=1):
                dori = db.user_dori(id=order[2])
                if dori:
                    user = db.select_user(id=order[1])
                    text += f"""🔹 Buyurtma {order[4]}
                    👤 Mijoz: {user[2]}
                    📞 Tel: {user[3]}
                    🆔 TG ID: {user[1]}
                    📍Manzil: {user[4]} {user[5]}
                    🛒 Mahsulotlar ({dori[1]}):"""
                    text += f"\n _________________________\n"
                    keyboard.insert(InlineKeyboardButton(text=f"{son}", callback_data=f"order1:{order[0]}"))
                    keyboard.row(
                        InlineKeyboardButton("◀", callback_data=f"page3:{page-1}"),
                        InlineKeyboardButton("▶", callback_data=f"page3:{page+1}"),)
                else:
                    db.delete_order(id=order[0])
            return text, keyboard
        else:
            return "Xozirda buyutmalar mavjud emas", keyboard
    except Exception as e:
        print(e)
