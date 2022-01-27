from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


async def create_keyboard(coins):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for address, symbol, name in coins:
        keyboard.insert(KeyboardButton(symbol.upper()))
    return keyboard
