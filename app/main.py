import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from modules.config import TLG_TOKEN, DB_PATH, API_RATE, API_PAIR
import sqlite3
import requests

from modules.TokenList import TokenList


class ExStates(StatesGroup):
    single = State()
    pair_first = State()
    pair_second = State()


class APIHandler:
    def __init__(self):
        self.api_rate = API_RATE
        self.api_pair = API_PAIR

    def output(self, address_1, address_2=None):
        if address_2 is None:
            return self.handle_one_address(address_1)
        else:
            return self.handle_pair_addresses(address_1, address_2)

    def handle_one_address(self, address):
        r = requests.get(f'{self.api_rate}/{address}')

        if 200 == r.status_code:
            return r.json()['data']
        else:
            raise Exception(f'API bad response. Http response code is {r.status_code}')

    def handle_pair_addresses(self, address_1, address_2):
        r1 = requests.get(f'{self.api_rate}/{address_1}')
        r2 = requests.get(f'{self.api_rate}/{address_2}')

        if 200 == r1.status_code and 200 == r2.status_code:
            return [(r1.json()['data'], r2.json()['data'])]
        else:
            raise Exception(f'API bad response. Http response code is {r1.status_code} and {r2.status_code} ')


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TLG_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

token_list = TokenList()
api_handler = APIHandler()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")




@dp.message_handler(commands=['single'], state='*')
async def single_rate(message: types.Message, state: FSMContext):
    await ExStates.single.set()
    await message.reply("Send a coin to get it's rate!")


@dp.message_handler(content_types=types.ContentType.TEXT, state=ExStates.single)
async def single_rate_reply(message: types.Message, state: FSMContext):
    addresses = token_list.output(message.text)

    if len(addresses) == 0:
        await message.reply('Unknown coin')
        await state.finish()
    elif len(addresses) == 1:
        await message.reply(api_handler.output(addresses[0][0]))
        await state.finish()
    else:
        # Сделать кнопки с возможными вариантами
        pass


@dp.message_handler(commands=['pair'])
async def pair_rate(message: types.Message, state: FSMContext):
    await ExStates.pair_first.set()
    await message.reply("Send a first coin from the pair!")


@dp.message_handler(content_types=types.ContentType.TEXT, state=ExStates.pair_first)
async def pair_first_coin(message: types.Message, state: FSMContext):
    addresses = token_list.output(message.text)

    if len(addresses) == 0:
        await message.reply('Unknown coin')
    elif len(addresses) == 1:
        await message.reply('Ok, now send me second coin!')
        async with state.proxy() as data:
            data['first_coin'] = addresses[0][0]
        await ExStates.pair_second.set()
    else:
        # Сделать кнопки с возможными вариантами
        pass


@dp.message_handler(content_types=types.ContentType.TEXT, state=ExStates.pair_second)
async def pair_second_coin(message: types.Message, state: FSMContext):
    addresses = token_list.output(message.text)

    if len(addresses) == 0:
        await message.reply('Unknown coin')
    elif len(addresses) == 1:
        async with state.proxy() as data:
            await message.reply(f'{api_handler.output(data["first_coin"], addresses[0][0])}')
        await state.finish()
    else:
        # Сделать кнопки с возможными вариантами
        pass


#@dp.message_handler()
#async def echo(message: types.Message):
#    # Добавить два состояния
#    # Переход в состояния по нажатию кнопки
#    await message.answer(token_list.output(message.text))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
