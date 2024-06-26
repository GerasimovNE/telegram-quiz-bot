import os
from dotenv import load_dotenv
from dal.telegramm_message import *
from dal.telegramm_db import create_table
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F

load_dotenv()
API_KEY = os.getenv('API_KEY')


logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_KEY)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message):
    await cmd_start(message)


@dp.message(F.text=="start")
@dp.message(Command("quiz"))
async def quiz(message: types.Message):
    await cmd_quiz(message)

@dp.message(F.text=="rating")
@dp.message(Command('rating'))
async def rating(message:types.Message):
    await cmd_rating(message)


@dp.callback_query()
async def ans(callback:types.CallbackQuery):
    await answer(callback)


async def main():
    await create_table()
    await create_table_result()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())