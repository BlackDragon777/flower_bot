from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = 'Your API TOKEN'
ADMIN_CHAT_ID = []


bot = Bot(API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

