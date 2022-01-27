from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TLG_TOKEN


# Initialize bot and dispatcher
bot = Bot(token=TLG_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

