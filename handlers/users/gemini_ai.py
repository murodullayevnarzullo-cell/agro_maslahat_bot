from aiogram import types
from loader import dp, model, chat_sessions
from io import BytesIO
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

class Usergemini(StatesGroup):
    start= State()


def get_chat(user_id):
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])
    return chat_sessions[user_id]

@dp.message_handler(text="🧑‍🌾 AI maslahati")
async def start_ai(msg: types.Message):
    await msg.answer(text="Assalomu alaykum qandey yordamin kerak yozishingiz mumkin. \nto'xtatish uchun /stop ni yuboring")
    await Usergemini.start.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=Usergemini.start)
async def bot_echo(message: types.Message):
    await message.answer_chat_action("typing")
    
    try:
        response = model.generate_content(message.text)
        
        if response.text:
            await message.answer(response.text, parse_mode=types.ParseMode.MARKDOWN)
        else:
            await message.answer("Kechirasiz, javob topilmadi.")
            
    except Exception as e:
        # Xatolikni terminalda ko'rish va foydalanuvchiga bildirish
        print(f"DEBUG ERROR: {e}")
        await message.answer("Tizimda vaqtinchalik uzilish yuz berdi. Birozdan so'ng urinib ko'ring.")

# Rasm uchun
@dp.message_handler(content_types=types.ContentType.PHOTO, state=Usergemini.start)
async def bot_image(message: types.Message):
    chat = get_chat(message.from_user.id)
    await message.answer_chat_action("typing")

    photo = message.photo[-1]
    photo_bytes = BytesIO()
    await photo.download(destination_file=photo_bytes)
    
    img_data = {"mime_type": "image/jpeg", "data": photo_bytes.getvalue()}
    prompt = message.caption if message.caption else "Ushbu rasmni tahlil qil."
    
    # Rasmni yuborish
    response = model.generate_content([prompt, img_data])
    
    # Tarixga qo'shish
    chat.history.append({"role": "user", "parts": [prompt]})    
    chat.history.append({"role": "model", "parts": [response.text]})
    
    await message.reply(response.text, parse_mode=types.ParseMode.MARKDOWN)