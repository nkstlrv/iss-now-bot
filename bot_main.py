from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils.markdown as md
import os
from dotenv import load_dotenv
import requests
import time

from calculations import iss_params, iss_crew

load_dotenv()

# ----------------------------------------------------------------------------------------------------------------------
# bot's code

bot = Bot(os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f'Hello there, <b>{message.chat.first_name}</b> 👋', parse_mode='HTML')
    await message.answer('This is <b>ISS Now</b> bot 🤖', parse_mode="HTML")
    await message.answer("My mission is to give you current "
                         "<i><b>International Space Station</b></i> data 🛰️ℹ️",
                         parse_mode='HTML')
    await message.answer('To call the <b>Main Menu</b> press 👉 /menu', parse_mode="HTML")


@dp.message_handler(commands=['menu'])
async def menu(message: types.Message):
    menu_markup = types.InlineKeyboardMarkup(row_width=2)

    b1 = types.InlineKeyboardButton('Location 📍🗺️', callback_data='location')
    b2 = types.InlineKeyboardButton('Parameters 📊', callback_data='params')
    b3 = types.InlineKeyboardButton('Crew 🧑‍🚀', callback_data='crew')
    b4 = types.InlineKeyboardButton('Live Cameras 🎥', callback_data='cameras')
    b5 = types.InlineKeyboardButton('Notify on Flyovers 💫', callback_data='notify')
    b6 = types.InlineKeyboardButton('Source Code', url='https://github.com/nkstlrv/iss-now-bot')

    menu_markup.row(b1, b2)
    menu_markup.row(b3, b4)
    menu_markup.row(b5)
    menu_markup.add(b6)

    await message.answer('⚙️ ISS Now menu', reply_markup=menu_markup)


@dp.callback_query_handler()
async def callback(call):
    await call.message.answer(call.data)


if __name__ == "__main__":
    executor.start_polling(dp)
