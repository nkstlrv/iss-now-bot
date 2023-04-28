from aiogram import Bot, Dispatcher, executor, types
import os
from dotenv import load_dotenv
import requests

from calculations import iss_params, iss_crew

load_dotenv()

# ----------------------------------------------------------------------------------------------------------------------
# bot's code

bot = Bot(os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Hello there 👋')


if __name__ == "__main__":
    executor.start_polling(dp)
