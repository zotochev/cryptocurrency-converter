from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from .ExStates import ExStates

from create_bot import dp, bot
from config import reactions
from keyboards import start_keyboard


async def send_other(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply(reactions['unknown_command'])
    await message.answer(reactions['help'])


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(send_other, state=None)
