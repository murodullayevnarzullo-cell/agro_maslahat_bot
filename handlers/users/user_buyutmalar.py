from aiogram import types
from loader import dp, db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery


@dp.message_handler(text="📦 Buyurtmalarim")
async def barcha_dorilar_buyutmalar(msg: types.Message):
    try:
        text, tugma = await buyutmalar_hammasi(tg_id=msg.from_user.id)
        await msg.answer(text=text, reply_markup=tugma)
    except Exception as e:
        print(e)

@dp.callback_query_handler(lambda call: "page2:" in call.data)
async def dorilar_buyutmalari(call: types.CallbackQuery):
    await call.message.answer(text=text, reply_markup=tugma)
    try:
        _, page = call.data.split(":")
        if int(page) > 0:
            text, tugma = await buyutmalar_hammasi(tg_id=call.from_user.id, page=page)
            if text:
                await call.message.delete()
                await call.message.answer(text=f"📋 {text}", reply_markup=tugma)
            else:
                await call.answer("Buyurtmalaringiz topilmadi")
        else:
            await call.answer("Buyurtmalaringiz topilmadi")
    except:
        await call.answer("Buyurtmalaringiz topilmadi")


@dp.callback_query_handler(lambda call: "order:" in call.data)
async def dorilar_buyutma_ochirish(call: types.CallbackQuery):
    try:
        _, dori_id = call.data.split(":")
        user_id = (db.select_users(call.from_user.id))[0]
        db.delete_order(id=dori_id)
        await call.answer("Buyurtmangiz bekor qilindi !")
        text, tugma = await buyutmalar_hammasi(tg_id=call.from_user.id)
        if text:
            await call.message.delete()
            await call.message.answer(text=f"📋 {text}", reply_markup=tugma)
        else:
            await call.answer("Buyurtmalar topilmadi")

    except Exception as e:
        print(e)
    


async def buyutmalar_hammasi(tg_id, page=1):
    try:
        user = db.select_users(telegram_id=tg_id)
        user_id = (user)[0]
        uzunlik = (db.orders_count(user_id=user_id))[0]
        if uzunlik+10 - page*10 >0:
            orders = db.select_order_user(user_id=user_id, page=page)
        else:
            orders = None
        keyboard = InlineKeyboardMarkup(row_width=3)
        if orders:
            keyboard = InlineKeyboardMarkup(row_width=5)
            s = page*10-10+1
            text = f"Buyurtmalar ro'yhati {s}-{page*10}: {uzunlik}. \n buyurtma bekor qilish uchun maxsulot raqamini bosing !"
            for son, order in enumerate(orders, start=1):
                dori = db.user_dori(id=order[2])
                if dori:
                    text += '\n' + f"{son}. id: {order[0]}"
                    text += f"\n name: {dori[1]}"
                    text += f"\n crop: {dori[2]}"
                    text += f"\n description: {dori[3]}"
                    text += f"\n price: {dori[4]}"
                    text += f"\n _________________________\n"
                    keyboard.insert(InlineKeyboardButton(text=f"{son}", callback_data=f"order:{order[0]}"))
                    keyboard.row(
                        InlineKeyboardButton("◀", callback_data=f"page2:{page-1}"),
                        InlineKeyboardButton("▶", callback_data=f"page2:{page+1}"),
                        )
                else:
                    db.delete_order(id=order[0])
            return text, keyboard
        else:
            return "Xozirda sizda buyutmalar mavjud emas", keyboard
    except Exception as e:
        print(e)
