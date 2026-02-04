from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import db, dp


class UserSupportState(StatesGroup):
    chatting = State()

@dp.message_handler(text="🧑‍🌾 Mutaxassis maslahati")
async def start_support(message: types.Message, state: FSMContext):
    await state.set_state(UserSupportState.chatting)
    await message.answer(
        "Mutaxassisga savolingizni yozing.\n"
        "📎 Rasm ham yuborishingiz mumkin.\n"
        "❌ Tugatish uchun /stop yozing."
    )

@dp.message_handler(state=UserSupportState.chatting, content_types=types.ContentType.TEXT)
async def user_text_message(message: types.Message):
    db.add_user_message(
        user_id=message.from_user.id,
        message_id=message.message_id,
        message_type="text"
    )

    await message.answer("✅ Xabaringiz qabul qilindi. \nyozishda savom etishimgiz mumkin")


@dp.message_handler(state=UserSupportState.chatting, content_types=types.ContentType.PHOTO)
async def user_photo_message(message: types.Message):
    db.add_user_message(
        user_id=message.from_user.id,
        message_id=message.message_id,
        message_type="photo"
    )

    await message.answer("📸 Rasm qabul qilindi \nyozishda savom etishimgiz mumkin")

@dp.message_handler(state=UserSupportState.chatting, content_types=[
    types.ContentType.VIDEO,
    types.ContentType.DOCUMENT,
    types.ContentType.VOICE
])
async def user_media_message(message: types.Message):
    db.add_user_message(
        user_id=message.from_user.id,
        message_id=message.message_id,
        message_type=message.content_type
    )

    await message.answer("📎 Fayl qabul qilindi")

