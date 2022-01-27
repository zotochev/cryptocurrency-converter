from aiogram import types
from aiogram.dispatcher import FSMContext
from ExStates import ExStates


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
