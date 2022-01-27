from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


async def create_keyboard(keys):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for key in keys:
        keyboard.insert(KeyboardButton(key))
    return keyboard
