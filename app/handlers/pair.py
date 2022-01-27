from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from handlers.ExStates import ExStates
from modules.TokenList import token_list
from modules.APIHandler import api_handler
from create_bot import dp, bot
from config import reactions



# @dp.message_handler(commands=['pair'])
async def pair_rate(message: types.Message, state: FSMContext):
    await ExStates.pair_first.set()
    await message.reply(reactions['pair'])


# @dp.message_handler(content_types=types.ContentType.TEXT, state=ExStates.pair_first)
async def pair_first_coin(message: types.Message, state: FSMContext):
    addresses = token_list.output(message.text)

    if len(addresses) == 0:
        await message.reply(reactions['unknown'])
    elif len(addresses) == 1:
        await message.answer(reactions['pair_next'])
        async with state.proxy() as data:
            data['first_coin'] = addresses[0]
        await ExStates.pair_second.set()
    else:
        # Сделать кнопки с возможными вариантами
        await message.reply(reactions['several'])


async def prepare_result_pair(output):
    result_price = float(output[0]['price']) / float(output[1]['price'])
    result_unit = f"{output[0]['symbol']}/{output[1]['symbol']}"
    return f"{result_price} {result_unit.upper()}"


# @dp.message_handler(content_types=types.ContentType.TEXT, state=ExStates.pair_second)
async def pair_second_coin(message: types.Message, state: FSMContext):
    addresses = token_list.output(message.text)

    if len(addresses) == 0:
        await message.reply(reactions['unknown'])
    elif len(addresses) == 1:
        await message.answer(reactions['pair_result'])
        async with state.proxy() as data:
            reply_message = await prepare_result_pair(api_handler.output(data["first_coin"][0], addresses[0][0]))
            await message.answer(reply_message)
        await state.finish()
    else:
        # Сделать кнопки с возможными вариантами
        await message.reply(reactions['several'])


def register_handlers_pair(dp: Dispatcher):
    dp.register_message_handler(pair_rate, commands=['pair'], state='*')
    dp.register_message_handler(pair_first_coin, content_types=types.ContentType.TEXT, state=ExStates.pair_first)
    dp.register_message_handler(pair_second_coin, content_types=types.ContentType.TEXT, state=ExStates.pair_second)

