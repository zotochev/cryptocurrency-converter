from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from handlers.ExStates import ExStates
from modules.TokenList import token_list
from modules.APIHandler import api_handler
from create_bot import dp, bot
from config import reactions
from keyboards import similar_coins


#@dp.message_handler(commands=['single'], state='*')
async def single_rate(message: types.Message, state: FSMContext):
    await ExStates.single.set()
    await message.reply(reactions['single'])


async def prepare_result_single(output):
    result_price = float(output[0]['price'])
    result_unit = f"{output[0]['symbol']}/USDT"
    return f"{result_price} {result_unit.upper()}"


#@dp.message_handler(content_types=types.ContentType.TEXT, state=ExStates.single)
async def single_rate_reply(message: types.Message, state: FSMContext):
    addresses = token_list.output(message.text)

    if len(addresses) == 0:
        await message.reply(reactions['unknown'])
        await state.finish()
    elif len(addresses) == 1:
        try:
            api_result = api_handler.output(addresses[0][0])
            reply_message = await prepare_result_single(api_result) 
            await message.answer(reactions['single_result'])
            await message.answer(reply_message)
        except UserWarning as e:
            await message.answer(reactions['api_bad_response'])
        await state.finish()
    else:
        # Сделать кнопки с возможными вариантами
        keyboard = await similar_coins.create_keyboard(addresses)
        await message.reply(reactions['several'], reply_markup=keyboard)


def register_handlers_single(dp: Dispatcher):
    dp.register_message_handler(single_rate, commands=['single'], state='*')
    dp.register_message_handler(single_rate_reply, content_types=types.ContentType.TEXT, state=ExStates.single)
