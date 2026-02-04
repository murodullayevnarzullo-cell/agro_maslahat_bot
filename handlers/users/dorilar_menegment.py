from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.admin_tugma import admin_main_menu, admin_medicines_menu, ogit_keyboard
from data.config import ADMINS
from loader import dp, db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters.state import State, StatesGroup

class AddMedicineState(StatesGroup):
    waiting_for_name = State()
    waiting_for_crop = State()
    waiting_for_description = State()
    waiting_for_price = State()

class EditMedicineState(StatesGroup):
    waiting_for_id = State()
    waiting_for_field = State()
    waiting_for_new_value = State()

class DeleteMedicineState(StatesGroup):
    waiting_for_id = State()



@dp.message_handler(text="🛒 O'g'itlar boshqaruvi")
async def dorilar_hendler(msg: types.Message):
    if str(msg.from_user.id) not in ADMINS:
        if not db.is_admin(msg.from_user.id):
            await msg.answer("Siz admin emassiz!")
            return
    text, tugma = await dorilar_hammasi()
    await msg.answer(text=text, reply_markup=tugma)


@dp.callback_query_handler(lambda call: call.data in ['medicine_add', 'medicine_delete', 'medicine_edit'])
async def dorilar_callback_handler(call: CallbackQuery, state: FSMContext):
    if str(call.from_user.id) not in ADMINS:
        if not db.is_admin(call.from_user.id):
            await call.answer("Siz admin emassiz!", show_alert=True)
            return

    if call.data == "medicine_add":
        await call.message.answer("Dori nomini kiriting: \nBekor qilish uchun /stop ni yuboring")
        await AddMedicineState.waiting_for_name.set()
        await call.answer()

    elif call.data == "medicine_edit":
        await call.message.answer("Tahrirlash uchun dori ID ni kiriting: \nBekor qilish uchun istalgan vaqtda /stop ni yuboring")
        await EditMedicineState.waiting_for_id.set()
        await call.answer()

    elif call.data == "medicine_delete":
        await call.message.answer("O‘chirish uchun dori ID ni kiriting: \nBekor qilish uchun istalgan vaqtda /stop ni yuboring")
        await DeleteMedicineState.waiting_for_id.set()
        await call.answer()


@dp.message_handler(state=DeleteMedicineState.waiting_for_id)
async def process_delete_dori(message: types.Message, state: FSMContext):
    try:
        id = int(message.text)
        db.delete_dori(id)

        await message.answer(f"{id} maxsulot o'chirildi o‘chirildi!")
    except Exception as e:
        await message.answer(f"Xatolik: {e}")
    await state.finish()


@dp.message_handler(state=AddMedicineState.waiting_for_name)
async def add_medicine_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("og'it turini tanlang?", reply_markup=ogit_keyboard())
    await AddMedicineState.waiting_for_crop.set()

@dp.callback_query_handler(lambda call: "ogit:" in call.data, state=AddMedicineState.waiting_for_crop)
async def add_medicine_crop(call: types.CallbackQuery, state: FSMContext):
    _, ogit = call.data.split(":")
    ogit = ogit.replace('📂 ', '')
    await call.message.delete()
    await state.update_data(crop=ogit)
    await call.message.answer("Dori haqida tavsif yozing:")
    await AddMedicineState.waiting_for_description.set()

@dp.message_handler(state=AddMedicineState.waiting_for_description)
async def add_medicine_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Narxini kiriting (raqam):")
    await AddMedicineState.waiting_for_price.set()

@dp.message_handler(state=AddMedicineState.waiting_for_price)
async def add_medicine_price(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
    except:
        await message.answer("Iltimos, narxni raqam sifatida kiriting:")
        return
    data = await state.get_data()
    db.add_medicine(
        name=data['name'],
        crop=data['crop'],
        description=data['description'],
        price=price
    )
    await message.answer(f"{data['name']} dori qo‘shildi!")
    await state.finish()


@dp.message_handler(state=EditMedicineState.waiting_for_id)
async def edit_medicine_id(message: types.Message, state: FSMContext):
    try:
        med_id = int(message.text)
    except:
        await message.answer("Iltimos, to‘g‘ri ID kiriting:")
        return
    await state.update_data(id=med_id)
    await message.answer("Qaysi maydonni o‘zgartirmoqchisiz? (name, crop, description, price)")
    await EditMedicineState.waiting_for_field.set()

@dp.message_handler(state=EditMedicineState.waiting_for_field)
async def edit_medicine_field(message: types.Message, state: FSMContext):
    field = message.text.lower()
    if field not in ['name','crop','description','price']:
        await message.answer("Faqat name, crop, description yoki price maydonini tanlang")
        return
    await state.update_data(field=field)
    await message.answer(f"Yangi qiymatni kiriting ({field}):")
    await EditMedicineState.waiting_for_new_value.set()

@dp.message_handler(state=EditMedicineState.waiting_for_new_value)
async def edit_medicine_value(message: types.Message, state: FSMContext):
    data = await state.get_data()
    value = message.text
    if data['field'] == 'price':
        try:
            value = int(value)
        except:
            await message.answer("Iltimos, narxni raqam sifatida kiriting:")
            return
    db.update_medicine(
        medicine_id=data['id'],
        name=value if data['field']=='name' else None,
        crop=value if data['field']=='crop' else None,
        description=value if data['field']=='description' else None,
        price=value if data['field']=='price' else None
    )
    await message.answer("Dori tahrirlandi!")
    await state.finish()


async def dorilar_hammasi(page=1):
    try:
        uzunlik = (db.dori_count())[0]
        if uzunlik+10 - page*10 >0:
            dorilar = db.select_all_dori(page=page)
        else:
            dorilar = None
        
        keyboard = InlineKeyboardMarkup(row_width=3)
        keyboard.add(
            InlineKeyboardButton("➕", callback_data="medicine_add"),
            InlineKeyboardButton("✏️", callback_data="medicine_edit"),
            InlineKeyboardButton("🗑", callback_data="medicine_delete"),
        )
        if dorilar:
            s = page*10-10+1
            text = f"dorilar ro'yhati {s}-{page*10}: {uzunlik}"
            for son, dori in enumerate(dorilar, start=1):
                text += '\n' + f"{son}. id: {dori[0]}"
                text += f"\n name: {dori[1]}"
                text += f"\n crop: {dori[2]}"
                text += f"\n description: {dori[3]}"
                text += f"\n price: {dori[4]}"
                text += f"\n _________________________\n"
            keyboard.row(
                InlineKeyboardButton("◀", callback_data=f"page1:{page-1}"),
                InlineKeyboardButton("▶", callback_data=f"page1:{page+1}"),
            )
            return text, keyboard
        else:
            return "Dorilarni boshqarish", keyboard
    except Exception as e:
        return 