from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os


# Initialize bot and dispatcher
bot = Bot(token=os.environ['TOKEN'])
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

