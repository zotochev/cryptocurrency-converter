from aiogram import executor
import asyncio

import logging

from create_bot import dp
from handlers import commands, single, pair, other


logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':

    commands.register_handlers_commands(dp)
    single.register_handlers_single(dp)
    pair.register_handlers_pair(dp)
    other.register_handlers_other(dp)
    
    executor.start_polling(dp, skip_updates=True)
