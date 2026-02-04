from aiogram import types
from loader import dp, db
from data.config import ADMINS
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

class AddAloqaState(StatesGroup):
    waiting_for_id = State()

@dp.message_handler(text="📞 Aloqa")
async def aloqa(msg: types.Message):
    try:
        malumot = db.select_all_aloqa()
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton(text="✏️", callback_data="add_aloqa")
            )
        if malumot:
            id, text = malumot[0], malumot[1]
        else:
            text = "Xozirda ma'lumotlar yo'q"
        if (str(msg.from_user.id) not in ADMINS) and (not db.is_admin(msg.from_user.id)):
            await msg.answer(text=text)
        else:
            await msg.answer(text=text, reply_markup=keyboard)
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data == "add_aloqa")
async def select_aloqa(call: types.CallbackQuery):
    try:
        text = "Aloqa ma'lumotlarini o'zgartirish uchun bu yerga yozing ! \n Bekor qilish uchun /stop ni yuboring"
        await AddAloqaState.waiting_for_id.set()
        await call.message.answer(text=text)
        await call.message.delete()
    except Exception as e:
        print(e)

@dp.message_handler(state=AddAloqaState.waiting_for_id)
async def add_aloqa(msg: types.Message, state: FSMContext):
    try:
        db.update_aloqa_status(matn=msg.text, id=1)
        await msg.answer("Aloqa ma'lumotlari yangilandi")
        await state.finish()
    except Exception as e:
        print(e)
