from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import db, dp, bot
from data.config import ADMINS
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class AdminSupportState(StatesGroup):
    chatting = State()

@dp.message_handler(commands="stops", state=AdminSupportState.chatting)
async def admin_stop_chat(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data['user_id']

    db.close_user_chat(user_id)

    await state.finish()
    await message.answer("✅ Yozishma yakunlandi")

@dp.message_handler(text="Savollarga javob")
async def admin_support_start(message: types.Message, state: FSMContext):
    try:
        if str(message.from_user.id) not in ADMINS:
            if not db.is_admin(message.from_user.id):
                await message.answer("Siz admin emassiz!")
                return
        text, keyboard = get_users_with_messages()
        await message.answer(text, reply_markup=keyboard)
    except Exception as e:
        print(e)


def get_users_with_messages():
    users = db.get_users_with_new_messages()
    if not users:
        return "Yangi murojaatlar yo‘q", None
    text = "📩 Foydalanuvchilar ro‘yxati:\n\n"
    keyboard = InlineKeyboardMarkup(row_width=1)

    for i, user in enumerate(users, start=1):
        user_id, fullname, status = user
        if str(user_id) not in ADMINS:
            if not db.is_admin(user_id):
                icon = "🆕" if status == "new" else "👀"

                text += f"{i}. [{icon}] {fullname}\n"
                keyboard.add(
                    InlineKeyboardButton(
                        text=f"{i}. {fullname}",
                        callback_data=f"admin_user:{user_id}"
                    ))

    return text, keyboard



@dp.callback_query_handler(lambda c: c.data.startswith("admin_user:"))
async def admin_open_chat(call: types.CallbackQuery, state: FSMContext):
    user_id = int(call.data.split(":")[1])

    await state.update_data(user_id=user_id)
    await state.set_state(AdminSupportState.chatting)

    messages = db.get_user_messages(user_id)

    if not messages:
        await call.message.answer("Xabarlar topilmadi")
        return

    for (msg_id,) in messages:
        await bot.copy_message(
            chat_id=call.from_user.id,
            from_chat_id=user_id,
            message_id=msg_id
        )

    db.mark_messages_seen(user_id)

    await call.message.answer(
        "✍️ Javob yozishingiz mumkin.\n"
        "❌ Tugatish uchun /stops"
    )


@dp.message_handler(state=AdminSupportState.chatting, content_types=types.ContentType.TEXT)
async def admin_text_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data['user_id']

    sent = await bot.send_message(user_id, message.text)

    db.add_admin_message(
        user_id=user_id,
        message_id=sent.message_id,
        message_type="text"
    )

@dp.message_handler(state=AdminSupportState.chatting, content_types=types.ContentType.PHOTO)
async def admin_photo_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data['user_id']

    sent = await bot.copy_message(
        chat_id=user_id,
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )

    db.add_admin_message(
        user_id=user_id,
        message_id=sent.message_id,
        message_type="photo"
    )


