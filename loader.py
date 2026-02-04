from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import google.generativeai as genai
from data import config
from utils.db_api.sql3 import Database

genai.configure(api_key=config.GEMINI_API_KEY)
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
genai.configure(api_key=config.GEMINI_API_KEY)



genai.configure(api_key=config.GEMINI_API_KEY)


# Eng xavfsiz va aniq nom bilan chaqirish
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=(
        "Siz 'Agro Maslahat' botisiz. Sizning asosiy vazifangiz foydalanuvchilarga "
        "qishloq xo'jaligi, o'simliklar parvarishi va huquqiy masalalarda yordam berishdir. "
        "Barcha savollarga FAQAT O'ZBEK TILIDA javob bering. Foydalanuvchi boshqa tilda yozsa ham, "
        "javobni o'zbek tiliga tarjima qilib qaytaring. Muloyim va professional bo'ling."
    )
)

chat_sessions = {}



storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database(path_to_db='data/main.db')
chat_sessions = {}

