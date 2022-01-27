from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from .ExStates import ExStates

from create_bot import dp, bot
from config import reactions
from keyboards import start_keyboard


# @dp.message_handler(commands=['start'])
async def send_start(message: types.Message, state: FSMContext):
    keyboard = await start_keyboard.create_keyboard(['/single', '/pair'])
    await state.finish()
    await message.answer(reactions['start'], reply_markup=keyboard)


async def send_help(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(reactions['help'])


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(send_start, commands=['start'], state='*')
    dp.register_message_handler(send_help, commands=['help'], state='*')
