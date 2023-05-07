import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
load_dotenv()

bot = Bot(os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher(bot)


class MainMenuMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton('Location 📍🗺️', callback_data='m-location')
    b2 = types.InlineKeyboardButton('Parameters 📊', callback_data='m-params')
    b3 = types.InlineKeyboardButton('Crew 🧑‍🚀', callback_data='m-crew')
    b4 = types.InlineKeyboardButton('Live Cameras 🎥', callback_data='m-cameras')
    b5 = types.InlineKeyboardButton('Notify on Flyovers 💫', callback_data='m-notify')
    b6 = types.InlineKeyboardButton("Bot's Source Code", url="https://github.com/nkstlrv/iss-now-bot")
    markup.row(b1, b2)
    markup.row(b3, b4)
    markup.row(b5)
    markup.add(b6)


class NavMarkup:
    mb = types.KeyboardButton("/menu \n⚙️ Main menu")
    nb = types.KeyboardButton("/notify \n🔔 Notifications menu")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(mb, nb)


class NotifyMarkup:
    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton('📍 Set Location', callback_data='n-loc')
    b2 = types.InlineKeyboardButton('✅ Notify', callback_data='n-on')
    b3 = types.InlineKeyboardButton('❌ Stop notifying', callback_data='n-off')
    b4 = types.InlineKeyboardButton('🗑️ Delete Account', callback_data='n-delete')
    markup.add(b1, b2, b3, b4)
