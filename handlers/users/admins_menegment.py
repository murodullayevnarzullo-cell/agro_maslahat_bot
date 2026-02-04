from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.admin_tugma import admin_main_menu, admin_list_menu
from data.config import ADMINS
from loader import dp, db
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class AddAdminState(StatesGroup):
    waiting_for_id = State()

class DeleteAdminState(StatesGroup):
    waiting_for_id = State()


@dp.message_handler(text="Adminlar ro'yxati")
async def admin_hendler(msg: types.Message):
    if str(msg.from_user.id) not in ADMINS:
        if not db.is_admin(msg.from_user.id):
            await msg.answer("Siz admin emassiz!")
            return
    

    text, tugma = await adminlar_hammasi()
    await msg.answer(text=text, reply_markup=tugma)

@dp.callback_query_handler(lambda call: "page1:" in call.data)
async def adminlar_hammasi1(call: types.CallbackQuery):
    await call.message.answer(text=text, reply_markup=tugma)
    try:
        _, page = call.data.split(":")
        if int(page) > 0:
            text, tugma = await adminlar_hammasi(page)
            if text:
                await call.message.delete()
                await call.message.answer(text=f"📋 {text}", reply_markup=tugma)
            else:
                await call.answer("Ma'lumotlar topilmadi")
        else:
            await call.answer("Ma'lumotlar topilmadi")
    except:
        await call.answer("Ma'lumotlar topilmadi")


@dp.callback_query_handler(lambda call: call.data in ['admin_add', 'admin_delete'])
async def admin_callback_handler(call: CallbackQuery, state: FSMContext):
    if str(call.from_user.id) not in ADMINS:
        if not db.is_admin(call.from_user.id):
            await call.answer("Siz admin emassiz!", show_alert=True)
            return

    elif call.data == "admin_add":
        await call.message.answer("Yangi admin qo'shish uchun telegram ID ni yuboring: \nBekor qilish uchun /stop ni yuboring")
        await AddAdminState.waiting_for_id.set()
        await call.answer()

    elif call.data == "admin_delete":
        admins = db.select_all_admins()
        text = "Adminlar ro'yxati:\n\n"
        for admin in admins:
            text += f"{admin[0]}. {admin[2]} (ID: {admin[1]})\n"
        text += "\nO'chirish uchun admin ID ni yuboring: \nBekor qilish uchun /stop ni yuboring"
        
        await call.message.answer(text)
        await DeleteAdminState.waiting_for_id.set()
        await call.answer()




@dp.message_handler(state=AddAdminState.waiting_for_id)
async def process_add_admin(message: types.Message, state: FSMContext):
    try:
        tg_id = int(message.text)
        db.add_admin(tg_id, "Admin")
        await message.answer(f"{tg_id} telegram ID bilan admin qo'shildi!")
    except Exception as e:
        await message.answer(f"Xatolik: {e}")
    await state.finish()

@dp.message_handler(state=DeleteAdminState.waiting_for_id)
async def process_delete_admin(message: types.Message, state: FSMContext):
    try:
        tg_id = int(message.text)
        if str(message.from_user.id) in ADMINS:
            db.delete_admin(tg_id)
            await message.answer(f"{tg_id} telegram ID bilan admin o‘chirildi!")
        else:
            await message.answer(f"siz Adminlarni o'chirish xuquqiga ega emassiz")
    except Exception as e:
        await message.answer(f"Xatolik: {e}")
    await state.finish()


async def adminlar_hammasi(page=1):
    try:
        uzunlik = (db.admin_count())[0]
        if uzunlik+10 - page*10 >0:
            adminlar = db.select_all_admin(page=page)
        else:
            adminlar = None
        
        keyboard = InlineKeyboardMarkup(row_width=3)
        keyboard.add(
            InlineKeyboardButton("➕", callback_data="admin_add"),
            InlineKeyboardButton("🗑", callback_data="admin_delete"),
        )
        if adminlar:
            
            s = page*10-10+1
            text = f"adminlar ro'yhati {s}-{page*10}: {uzunlik}"
            for son, admin in enumerate(adminlar, start=1):
                text += '\n' + f"{son}. id: {admin[0]}"
                text += f"\n telegram_id: {admin[1]}"
                text += f"\n _________________________\n"
            keyboard.row(
                InlineKeyboardButton("◀", callback_data=f"page1:{page-1}"),
                InlineKeyboardButton("▶", callback_data=f"page1:{page+1}"),
            )
            return text, keyboard
        else:
            return "adminlarni boshqarish", keyboard
    except Exception as e:
        return 