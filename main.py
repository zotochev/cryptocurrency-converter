import logging
from aiogram import Bot, Dispatcher, executor, types

from config import TOKEN as API_TOKEN
import sqlite3
from SQLighter import SQLighter
import requests


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

db_worker = SQLighter('tokens.db')


def get_price(address):
    r = requests.get(f'https://api.pancakeswap.info/api/v2/tokens/{address}')
    if 200 == r.status_code:
        data = r.json()['data']
        print(data)
        return f"name: {data['name']}\nprice: {data['price']}\nprice_bnb: {data['price_BNB']}"
    else:
        return 'Error'


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler()
async def echo(message: types.Message):
    # message.text
    #   проверить является ли он адресом (начинается с '0x'),
    #   попробовать найти message.text в базе данных в поляях name или symbol
    if message.text[:2] == '0x':
        address = message.text
    else:
        address = db_worker.find_token(message.text.lower())[0]

    await message.answer(get_price(address))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
