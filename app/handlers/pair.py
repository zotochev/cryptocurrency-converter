from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from handlers.ExStates import ExStates
from modules.TokenList import token_list
from modules.APIHandler import api_handler
from create_bot import dp, bot
from config import reactions
from keyboards import similar_coins


# /pair command handler located in commands.py

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
        keyboard = await similar_coins.create_keyboard(addresses)
        await message.reply(reactions['several'], reply_markup=keyboard)



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
        try:
            async with state.proxy() as data:
                api_result = api_handler.output(data["first_coin"][0], addresses[0][0])
                reply_message = await prepare_result_pair(api_result) 
            await message.answer(reactions['pair_result'])
            await message.answer(reply_message)

            await ExStates.pair_first.set()
            await message.answer(reactions['pair'])
        except UserWarning as e:
            await message.answer(reactions['api_bad_response'])
    else:
        keyboard = await similar_coins.create_keyboard(addresses)
        await message.reply(reactions['several'], reply_markup=keyboard)


def register_handlers_pair(dp: Dispatcher):
    dp.register_message_handler(pair_first_coin, content_types=types.ContentType.TEXT, state=ExStates.pair_first)
    dp.register_message_handler(pair_second_coin, content_types=types.ContentType.TEXT, state=ExStates.pair_second)

