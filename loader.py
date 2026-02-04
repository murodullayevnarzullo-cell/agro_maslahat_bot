from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import google.generativeai as genai
from data import config
from utils.db_api.sql3 import Database

genai.configure(api_key=config.GEMINI_API_KEY)
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
genai.configure(api_key=config.GEMINI_API_KEY)



genai.configure(api_key=config.GEMINI_API_KEY)

print("--- Ruxsat etilgan modellar ro'yxati ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Mavjud model: {m.name}")
except Exception as e:
    print(f"Modellarni olishda xatolik: {e}")

# Eng xavfsiz va aniq nom bilan chaqirish
model = genai.GenerativeModel('models\gemini-2.5-flash')

chat_sessions = {}



storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database(path_to_db='data/main.db')
chat_sessions = {}

