from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.tugmalar import user_main_menu, phone_keyboard, user_main_menu, admin_main_menu
from keyboards.inline.user_inline_tugma import district_keyboard
from data.config import ADMINS
from aiogram.dispatcher import FSMContext
from loader import dp, db
from aiogram.dispatcher.filters.state import State, StatesGroup
import re
class UserSupportState(StatesGroup):
    chatting = State()


pattern = r'^(\+998|998)?[\s-]?(90|91|93|94|95|97|98|99|33|88)[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$'

def is_valid_uz_phone(phone: str) -> bool:
    return bool(re.match(pattern, phone))



class UserRegisterState(StatesGroup):
    district = State()
    mfy = State()
    phone = State()



@dp.message_handler(commands="stop", state=UserSupportState.chatting)
async def stop_support(message: types.Message, state: FSMContext):
    db.close_user_chat(message.from_user.id)

    await state.finish()
    await message.answer(
        "✅ Mutaxassis bilan yozishma yakunlandi.\n"
        "Tez orada javob beriladi.",
        reply_markup=user_main_menu()
    )


@dp.message_handler(text="/stop",state='*')
async def stop_state(message: types.Message, state: FSMContext):
    await message.answer("jarayon yakunlandi !")
    await state.finish()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if str(message.from_user.id) in ADMINS or db.is_admin(message.from_user.id):
        await message.answer(f"Assalomu alaykum, {message.from_user.full_name}! \nBo'limlardan birini tanlang", reply_markup=admin_main_menu())
    else:
        if db.select_users(message.from_user.id):
            await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!", reply_markup=user_main_menu())
        else:
            await message.answer(
                "👋 Xush kelibsiz!\n\nIltimos, tumanni tanlang:",
                reply_markup=district_keyboard()
            )
            await UserRegisterState.district.set()

@dp.callback_query_handler(lambda c: c.data.startswith("district:"), state=UserRegisterState.district)
async def select_district(call: types.CallbackQuery, state: FSMContext):
    district = call.data.split(":")[1]
    await state.update_data(district=district)

    await call.message.answer(
        "🏘 MFY nomini qo‘lda kiriting:\n\nMasalan: \"Yangi hayot MFY\""
    )
    await UserRegisterState.mfy.set()


@dp.message_handler(state=UserRegisterState.mfy)
async def input_mfy(message: types.Message, state: FSMContext):
    mfy = message.text.strip()

    if len(mfy) < 3:
        await message.answer("❗ MFY nomi juda qisqa, qayta kiriting:")
        return

    await state.update_data(mfy=mfy)

    await message.answer(
        "📞 Telefon raqamingizni yuboring:",
        reply_markup=phone_keyboard()
    )
    await UserRegisterState.phone.set()

@dp.message_handler(content_types=types.ContentType.CONTACT, state=UserRegisterState.phone)
async def input_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    db.add_user(
        telegram_id=message.from_user.id,
        fullname = message.from_user.first_name,
        phone=message.contact.phone_number,
        district=data['district'],
        mfy=data['mfy']
        
    )
    await message.answer(
        "✅ Ro'yxatdan muvaffaqiyatli o'tdingiz!",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        "🏠 Asosiy menyu",
        reply_markup=user_main_menu()
    )

    await state.finish()


@dp.message_handler(state=UserRegisterState.phone)
async def input_phone(message: types.Message, state: FSMContext):
    try:
        if is_valid_uz_phone(message.text):
            data = await state.get_data()
            db.add_user(
                telegram_id=message.from_user.id,
                fullname = message.from_user.first_name,
                phone=message.contact.phone_number,
                district=data['district'],
                mfy=data['mfy']
                
            )
            await message.answer(
                "✅ Ro'yxatdan muvaffaqiyatli o'tdingiz!",
                reply_markup=ReplyKeyboardRemove()
            )
            await message.answer(
                "🏠 Asosiy menyu",
                reply_markup=user_main_menu()
            )

            await state.finish()
        else:
            await message.answer(text="Telefon raqamingizni qayta kiriting")
    except:
        await message.answer(text="Telefon raqamingizni qayta kiriting")