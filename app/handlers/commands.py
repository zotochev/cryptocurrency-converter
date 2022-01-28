from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from schedule import run_pending

from .ExStates import ExStates

from create_bot import dp, bot
from config import reactions
from keyboards import start_keyboard
import os


# @dp.message_handler(commands=['start'])
async def send_start(message: types.Message, state: FSMContext):
    keyboard = await start_keyboard.create_keyboard(['/single', '/pair'])
    await state.finish()
    await message.answer(reactions['start'], reply_markup=keyboard, parse_mode='markdown', disable_web_page_preview=True)

    # update token list
    run_pending()


# @dp.message_handler(commands=['help'])
async def send_help(message: types.Message, state: FSMContext):
    await message.reply(reactions['help'])


# @dp.message_handler(commands=['single'], state='*')
async def single_rate(message: types.Message, state: FSMContext):
    await ExStates.single.set()
    await message.reply(reactions['single'])


# @dp.message_handler(commands=['pair'])
async def pair_rate(message: types.Message, state: FSMContext):
    await ExStates.pair_first.set()
    await message.reply(reactions['pair'])


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(send_start, commands=['start'], state='*')
    dp.register_message_handler(send_help, commands=['help'], state='*')
    dp.register_message_handler(single_rate, commands=['single'], state='*')
    dp.register_message_handler(pair_rate, commands=['pair'], state='*')
