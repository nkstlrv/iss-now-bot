import os
import sqlite3
import time

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from background_tasks.updater import schedule_jobs
from functions import iss_params, iss_crew, unix_time_converter, geocoding
from functions.user_ids_from_db import get_all_ids, get_ids_to_notify

load_dotenv()

bot = Bot(os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher(bot)


# Start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f'Hello there, <b>{message.chat.first_name}</b> 👋', parse_mode='HTML')
    time.sleep(1)
    await message.answer('This is <b>ISS Now</b> bot 🤖', parse_mode="HTML")
    time.sleep(1)
    await message.answer('To call the <b>Main Menu</b> press 👉 /menu', parse_mode="HTML")


# Main Menu
@dp.message_handler(commands=['menu'])
async def menu(message: types.Message):
    menu_markup = types.InlineKeyboardMarkup(row_width=2)

    b1 = types.InlineKeyboardButton('Location 📍🗺️', callback_data='m-location')
    b2 = types.InlineKeyboardButton('Parameters 📊', callback_data='m-params')
    b3 = types.InlineKeyboardButton('Crew 🧑‍🚀', callback_data='m-crew')
    b4 = types.InlineKeyboardButton('Live Cameras 🎥', callback_data='m-cameras')
    b5 = types.InlineKeyboardButton('Notify on Flyovers 💫', callback_data='m-notify')
    b6 = types.InlineKeyboardButton('Source Code', url='https://github.com/nkstlrv/iss-now-bot')

    menu_markup.row(b1, b2)
    menu_markup.row(b3, b4)
    menu_markup.row(b5)
    menu_markup.add(b6)

    await message.answer('⚙️ ISS Now menu', reply_markup=menu_markup)


# Main Menu callback handler
@dp.callback_query_handler(text_startswith="m")
async def callback(call):
    async def coordinates_converter():
        lat = iss_params.iss_data()['lat']
        lng = iss_params.iss_data()['lng']

        if lat < 0:
            lat = f"{round(lat, 3) * -1}° S"
        else:
            lat = f"{round(lat, 3)}° N"

        if lng < 0:
            lng = f"{round(lng, 3) * -1}° W"
        else:
            lng = f"{round(lng, 3)}° E"

        return {'lat': lat, 'lng': lng}

    if call.data == 'm-location':
        coordinates = await coordinates_converter()
        await bot.send_message(call.from_user.id, f"🌍 International Space Station "
                                                  f"now at: \n\n<i>latitude</i> - {coordinates['lat']}\n"
                                                  f"<i>longitude</i> - {coordinates['lng']}", parse_mode='HTML')
        await bot.send_location(call.from_user.id,
                                latitude=iss_params.iss_data()['lat'],
                                longitude=iss_params.iss_data()['lng'])
        await bot.send_message(call.from_user.id, "Return to the \n⚙️ <b>Main Menu</b> 👉 /menu", parse_mode='HTML')

    elif call.data == 'm-params':
        await bot.send_message(call.from_user.id, f"📊 International Space Station parameters:", parse_mode='HTML')
        await bot.send_message(call.from_user.id,
                               f"<b><i>Velocity</i></b>:   {iss_params.iss_data()['v_mps']} m/s"
                               f"  | {iss_params.iss_data()['v_kph']} km/h\n\n"
                               f"<b><i>Altitude</i></b>:   {iss_params.iss_data()['alt']} km\n\n"
                               f"<b><i>Earth side</i></b>:   {iss_params.iss_data()['vis']}\n\n"
                               f"<b><i>People on board</i></b>:   {iss_crew.people_iss()['num']}",
                               parse_mode='HTML')
        await bot.send_message(call.from_user.id, "Return to the \n⚙️ <b>Main Menu</b> 👉 /menu", parse_mode='HTML')

    elif call.data == 'm-crew':
        await bot.send_message(call.from_user.id, f"🧑‍🚀 There are <b>{iss_crew.people_iss()['num']}</b> people"
                                                  f" on board now",
                               parse_mode='html')
        await bot.send_message(call.from_user.id, f"Here is a list of them:",
                               parse_mode='html')

        for name in iss_crew.people_iss()['people']:
            await bot.send_message(call.from_user.id, f"{name}", parse_mode='html')

        await bot.send_message(call.from_user.id, "Return to the \n⚙️ <b>Main Menu</b> 👉 /menu", parse_mode='HTML')

    elif call.data == 'm-cameras':
        await bot.send_message(call.from_user.id, f"To choose live camera press 👉 /cameras")

    elif call.data == 'm-notify':
        await bot.send_message(call.from_user.id,
                               "To open 🔔 <b>Notifications menu</b>\n press 👉 /notify", parse_mode='html')


# Cameras Menu
@dp.message_handler(commands=['cameras'])
async def menu(message: types.Message):
    camera_markup = types.InlineKeyboardMarkup(row_width=1)

    camera_markup.add(types.InlineKeyboardButton('🌎 Earth Cam', callback_data='earth'))
    camera_markup.add(types.InlineKeyboardButton('🛰️ Space Station Cam', callback_data='station'))
    camera_markup.add(types.InlineKeyboardButton('📺 NASA Live TV', callback_data='tv'))

    await message.answer('🎥 Live Cameras', reply_markup=camera_markup)


# Cameras callback handler
@dp.callback_query_handler(lambda call: call.data == "earth" or call.data == "station" or call.data == 'tv')
async def callback(call):
    if call.data == 'earth':
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


# Notifications Menu
@dp.message_handler(commands=['notify'])
async def menu(message: types.Message):
    db = sqlite3.connect("data/iss_now.db")
    c = db.cursor()

    notify_markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton('📋 Sign Up', callback_data='n-sign-up')
    b2 = types.InlineKeyboardButton('✅ On notifications', callback_data='n-on')
    b3 = types.InlineKeyboardButton('❌ Off notifications', callback_data='n-off')
    b4 = types.InlineKeyboardButton('📍 Update Location', callback_data='n-update')
    b5 = types.InlineKeyboardButton('🗑️ Delete Account', callback_data='n-delete')

    ids = get_all_ids()

    if message.from_user.id in ids:

        c.execute("""SELECT do_notify FROM config 
                    WHERE id == (?)""", (message.from_user.id,))
        do_notify = c.fetchall()[0][0]

        if do_notify == 0:
            notify_markup.add(b2, b4, b5)
        else:
            notify_markup.add(b3, b4, b5)

    else:
        notify_markup.add(b1)

    await message.answer('🔔 Notifications Menu 🛠️', reply_markup=notify_markup)

    db.close()


# Notifications callback handler
@dp.callback_query_handler(text_startswith="n")
async def callback(call):
    db = sqlite3.connect("data/iss_now.db")
    c = db.cursor()

    if call.data == 'n-sign-up':
        b1 = types.KeyboardButton("🗺️ Share Location", request_location=True)
        b2 = types.KeyboardButton("⛔ Stop registration")
        loc_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True).add(b1, b2)

        await bot.send_message(call.from_user.id,
                               "To Sign Up, I need your 📍 <b>location</b> first\n\n"
                               "Just press the <b>Share Location</b> button 👇",
                               parse_mode='html', reply_markup=loc_markup)

    elif call.data == 'n-delete':
        c.execute("""
            DELETE FROM config
            WHERE id == (?)
        """, (call.from_user.id,))

        db.commit()

        await bot.send_message(call.from_user.id, "Your account was successfully deleted 🗑️")
        time.sleep(1)
        await bot.send_message(call.from_user.id, "🔔 Notifications Setup Menu 🛠️ 👉 /notify \n\n"
                                                  "<b>Main Menu</b> 👉 /menu", parse_mode='HTML')

    elif call.data == 'n-update':
        b1 = types.KeyboardButton("🗺️ New Location", request_location=True)
        b2 = types.KeyboardButton("⛔ Stop Update")
        loc_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True).add(b1, b2)

        await bot.send_message(call.from_user.id,
                               "To Update location just press <b>New Location</b> button 👇",
                               parse_mode='html', reply_markup=loc_markup)

    elif call.data == 'n-on':
        c.execute("""
                    UPDATE config
                    SET do_notify = 1
                    WHERE id == (?);
                """, (call.from_user.id,))

        db.commit()

        await bot.send_message(call.from_user.id, "Notifications Turned On ✅")
        time.sleep(1)
        await bot.send_message(call.from_user.id, "🔔 Notifications Setup Menu 🛠️ 👉 /notify \n\n"
                                                  "<b>Main Menu</b> 👉 /menu", parse_mode='HTML')

    elif call.data == 'n-off':
        c.execute("""
                    UPDATE config
                    SET do_notify = 0
                    WHERE id == (?);
                """, (call.from_user.id,))

        db.commit()

        await bot.send_message(call.from_user.id, "Notifications Turned Off ❌")
        time.sleep(1)
        await bot.send_message(call.from_user.id, "🔔 Notifications Setup Menu 🛠️ 👉 /notify \n\n"
                                                  "<b>Main Menu</b> 👉 /menu", parse_mode='HTML')

    db.close()


# Location Setup and Update handler
@dp.message_handler(content_types=['location'])
async def menu(message: types.Message):
    user_lat = message.location.latitude
    user_lng = message.location.longitude
    await message.reply("Location received ✔️", reply_markup=types.ReplyKeyboardRemove())
    time.sleep(1)

    db = sqlite3.connect("data/iss_now.db")
    c = db.cursor()

    ids = get_all_ids()

    user_id = message.from_user.id

    try:
        user_username = message.from_user.username
    except Exception:
        user_username = None

    user_f_name = message.from_user.first_name

    if user_id in ids:
        c.execute("""
                    UPDATE config
                    SET lat = (?), lng = (?), last_notified = 1
                    WHERE id == (?);
                """, (user_lat, user_lng, user_id))

        db.commit()
        await message.answer("Location updated ✅")
        time.sleep(1)
        await message.answer("🔔 Notifications Setup Menu 🛠️ 👉 /notify \n\n"
                             "<b>Main Menu</b> 👉 /menu", parse_mode='HTML')

    else:
        c.execute("""
                           INSERT INTO config (id, username, f_name, lat, lng) 
                           VALUES (?, ?, ?, ?, ?)
               """, (user_id, user_username, user_f_name, user_lat, user_lng))
        db.commit()

        await message.answer("Registration completed ✅")
        time.sleep(1)
        await message.answer("🔔 Notifications Setup Menu 🛠️ 👉 /notify \n\n"
                             "<b>Main Menu</b> 👉 /menu", parse_mode='HTML')

    db.close()


# Notifies every user during ISS flyover at their location
async def notify_users(dp: Dispatcher):
    db = sqlite3.connect("data/iss_now.db")
    c = db.cursor()

    users_to_notify = get_ids_to_notify()

    for user in users_to_notify:

        c.execute("""
        
            SELECT lat, lng FROM config
            WHERE id == (?) AND last_notified < ((?) - 1080);
        
        """, (user, int(time.time())))

        data = c.fetchall()
        iss_data = iss_params.iss_data()

        if len(data) > 0:

            try:
                user_coordinates = (data[0][0], data[0][1])
                iss_coordinates = (iss_data['lat'], iss_data['lng'])

                dist = geocoding.get_distance(user_coordinates, iss_coordinates)
                # dist = 200

                if dist <= 600 and "N" in iss_data['vis']:
                    await dp.bot.send_message(user, "⚠️ ISS <b>Flyover now</b> ! 🔥", parse_mode='html')
                    await dp.bot.send_location(user, latitude=iss_coordinates[0], longitude=iss_coordinates[1])

                    print(f"{user} notified at {unix_time_converter.unix_converter(time.time())}")

                    c.execute("""
                    UPDATE config
                    SET last_notified = (?)
                    WHERE id == (?);
                    """, (int(time.time()), user))

                    db.commit()

            except Exception as e:
                print(e)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=schedule_jobs(notify_users, dp),
                           on_shutdown=sqlite3.connect("data/iss_now.db").close())
