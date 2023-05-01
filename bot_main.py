from aiogram import Bot, Dispatcher, executor, types
import os
from dotenv import load_dotenv
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
    await message.answer("My mission is to supply you with current data about\n"
                         "<a href='https://www.wikiwand.com/en/International_Space_Station'><b>"
                         "International Space Station</b></a>",
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
    async def coordinates_converter():
        lat = await iss_params.iss_data()['lat']
        lng = await iss_params.iss_data()['lng']

        if lat < 0:
            lat = f"{round(lat, 3) * -1}° S"
        else:
            lat = f"{round(lat, 3)}° N"

        if lng < 0:
            lng = f"{round(lng, 3) * -1}° W"
        else:
            lng = f"{round(lng, 3)}° E"

        return {'lat': lat, 'lng': lng}

    if call.data == 'location':
        coordinates = await coordinates_converter()
        await bot.send_message(call.from_user.id, f"🌍 International Space Station "
                                                  f"now at: \n\n<i>latitude</i> - {coordinates['lat']}\n"
                                                  f"<i>longitude</i> - {coordinates['lng']}", parse_mode='HTML')
        await bot.send_location(call.from_user.id,
                                latitude=await iss_params.iss_data()['lat'],
                                longitude=await iss_params.iss_data()['lng'])
        await bot.send_message(call.from_user.id, "Return to the \n⚙️ <b>Main Menu</b> 👉 /menu", parse_mode='HTML')

    elif call.data == 'params':
        await bot.send_message(call.from_user.id, f"📊 International Space Station parameters:", parse_mode='HTML')
        await bot.send_message(call.from_user.id, f"<b><i>Velocity</i></b>:   {await iss_params.iss_data()['v_mps']} m/s"
                                                  f"  | {await iss_params.iss_data()['v_kph']} km/h\n\n"
                                                  f"<b><i>Altitude</i></b>:   {await iss_params.iss_data()['alt']} km\n\n"
                                                  f"<b><i>Earth side</i></b>:   {await iss_params.iss_data()['vis']}\n\n"
                                                  f"<b><i>People on board</i></b>:   {await iss_crew.people_iss()['num']}",
                               parse_mode='HTML')
        await bot.send_message(call.from_user.id, "Return to the \n⚙️ <b>Main Menu</b> 👉 /menu", parse_mode='HTML')

    elif call.data == 'crew':
        await bot.send_message(call.from_user.id, f"🧑‍🚀 There are <b>{await iss_crew.people_iss()['num']}</b> people"
                                                  f" on board now",
                               parse_mode='html')
        await bot.send_message(call.from_user.id, f"Here is a list of them:",
                               parse_mode='html')

        for name in await iss_crew.people_iss()['people']:
            await bot.send_message(call.from_user.id, f"{name}", parse_mode='html')

        await bot.send_message(call.from_user.id, "Return to the \n⚙️ <b>Main Menu</b> 👉 /menu", parse_mode='HTML')

    elif call.data == 'cameras':
        await bot.send_message(call.from_user.id, f"To choose live camera press 👉 /cameras")

    elif call.data == 'earth':
        await bot.send_message(call.from_user.id, "Live view on Earth from ISS\n\n"
                                                  "https://www.youtube.com/live/itdpuGHAcpg?feature=share")
        await bot.send_message(call.from_user.id, "Return to the \n⚙️ <b>Main Menu</b> 👉 /menu", parse_mode='HTML')

    elif call.data == 'station':
        await bot.send_message(call.from_user.id, "Live view on the International Space Station\n\n"
                                                  "https://www.youtube.com/live/xAieE-QtOeM?feature=share")
        await bot.send_message(call.from_user.id, "Return to the \n⚙️ <b>Main Menu</b> 👉 /menu", parse_mode='HTML')

    elif call.data == 'tv':
        await bot.send_message(call.from_user.id, "NASA Live TV\n\n"
                                                  "https://www.youtube.com/live/21X5lGlDOfg?feature=share")
        await bot.send_message(call.from_user.id, "Return to the \n⚙️ <b>Main Menu</b> 👉 /menu", parse_mode='HTML')


@dp.message_handler(commands=['cameras'])
async def menu(message: types.Message):
    camera_markup = types.InlineKeyboardMarkup(row_width=1)

    camera_markup.add(types.InlineKeyboardButton('🌎 Earth Cam', callback_data='earth'))
    camera_markup.add(types.InlineKeyboardButton('🛰️ Space Station Cam', callback_data='station'))
    camera_markup.add(types.InlineKeyboardButton('📺 NASA Live TV', callback_data='tv'))

    await message.answer('🎥 Live Cameras', reply_markup=camera_markup)


if __name__ == "__main__":
    executor.start_polling(dp)
