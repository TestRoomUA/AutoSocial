# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from core.handlers.basic import get_start, get_photo, get_hello, get_repeat, get_sticker, get_voice, get_location, get_inline
from core.filters.iscontact import IsTrueContact
from core.handlers.contact import get_fake_contact, get_true_contact
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio
import logging
from core.settings import settings
from aiogram.filters import Command, CommandStart
from core.utils.commands import set_commands
from core.handlers.callback import select_car, select_start
from core.utils.callbackdata import CarInfo
from core.handlers.pay import order, pre_checkout_query, successful_payment, shipping_check
from core.middlewares.countermiddleware import CounterMiddleware
from core.middlewares.officehours import OfficeHoursMiddleware
from core.middlewares.dbmiddleware import DbSession
from core.middlewares.apschedulermiddleware import SchedulerMiddleware
import psycopg_pool  # asyncpg
from core.handlers import form
from core.utils.statesform import StepsForm
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.handlers import apsched
from datetime import datetime, timedelta
from core.handlers import send_media
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Bot started!')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Bot stopped')


def create_pool():  # async
    return psycopg_pool.AsyncConnectionPool(f"host='database-3.cl20yqscghpa.eu-north-1.rds.amazonaws.com' port=5432 dbname=postgres user=postgres password=0CoKbFUL1IcxnIN1Ipeg "
                                            f"connect_timeout=60")
    # return await asyncpg.create_pool(user='postgres',
    #                                  host='database-3.cl20yqscghpa.eu-north-1.rds.amazonaws.com',
    #                                  password='0CoKbFUL1IcxnIN1Ipeg',
    #                                  database='postgres',
    #                                  port=5432,
    #                                  # charset='utf8mb4',
    #                                  command_timeout=60)


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                                "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )
    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    pool_connect = create_pool()
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone="Europe/Warsaw")
    # scheduler.add_job(apsched.send_message_time, trigger='date', run_date=datetime.now() + timedelta(seconds=10),
    #                   kwargs={'bot': bot})
    # scheduler.add_job(apsched.send_message_cron, trigger='cron', hour=datetime.now().hour, minute=datetime.now().minute + 1,
    #                   start_date=datetime.now(), kwargs={'bot': bot})
    # scheduler.add_job(apsched.send_message_interval, trigger='interval', seconds=60, kwargs={'bot': bot})
    scheduler.start()

    dp.update.middleware.register(DbSession(pool_connect))
    dp.message.middleware.register(CounterMiddleware())
    dp.message.middleware.register(OfficeHoursMiddleware())  # dp.update
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(send_media.get_audio, Command(commands='audio'))
    dp.message.register(send_media.get_document, Command(commands='document'))
    dp.message.register(send_media.get_media_group, Command(commands='mediagroup'))
    dp.message.register(send_media.get_photo, Command(commands='photo'))
    dp.message.register(send_media.get_sticker, Command(commands='sticker'))
    dp.message.register(send_media.get_video, Command(commands='video'))
    dp.message.register(send_media.get_video_note, Command(commands='video_note'))
    dp.message.register(send_media.get_voice, Command(commands='voice'))

    dp.message.register(form.get_form, Command(commands='form'))
    dp.message.register(form.get_name, StepsForm.GET_NAME)
    dp.message.register(form.get_last_name, StepsForm.GET_LAST_NAME)
    dp.message.register(form.get_age, StepsForm.GET_AGE)

    dp.message.register(order, Command(commands='pay'))
    dp.pre_checkout_query.register(pre_checkout_query)
    dp.message.register(successful_payment, F.content_type == ContentType.SUCCESSFUL_PAYMENT)
    dp.shipping_query.register(shipping_check)
    dp.message.register(get_location, F.location)
    dp.message.register(get_photo, F.photo)
    dp.message.register(get_sticker, F.sticker)
    dp.message.register(get_voice, F.voice)
    dp.message.register(get_hello, F.text.lower() == 'hello')
    dp.message.register(get_true_contact, F.contact, IsTrueContact())
    dp.message.register(get_fake_contact, F.contact)
    dp.message.register(get_inline, Command(commands='inline'))
    dp.callback_query.register(select_car, CarInfo.filter(F.brand == 'Nissan'))
    dp.callback_query.register(select_start, F.data.startswith('start_'))
    dp.message.register(get_start, CommandStart())
    dp.message.register(form.get_form, F.text.lower() == 'анкета')
    dp.message.register(get_repeat)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())


















# def test(params):
#     city = params[0]
#     if city in ["", " "]:
#         city = input("dont understand:( Can you write city here: ")
#     response = requests.get(f'http://api.weatherapi.com/v1/current.json?key=3a30e305fa724e968e0184025240803&q={city}&aqi=no')
#     data = response.json()
#
#     _city = data["location"]['name']
#     time = data["current"]['last_updated']
#     temp = data['current']['temp_c']
#     print(f'{_city}, {time}. Temperature is {temp}C°')
#
#
# def weather(params):
#     match params[0]:
#         case "now":
#             test()
#         case _:
#             test()


# def get_data(filepath):
#     data = {}
#     if not os.path.isfile(filepath):
#         with open(filepath, "x") as f:
#             print("file is created")
#     else:
#         with open(filepath, "r") as f:
#             data = json.load(f)
#         print("...Data waiting...")
#     if data == {}:
#         data = json.dumps({"accounts": []}, indent=4)
#     if len(data["accounts"]) == 0:
#         print("...Creating first acc..")
#         add_exist_acc(input("Input Username: "), input("Input Password: "), filepath)
#
#     print("...print Data...")
#     for i in range(len(data["accounts"])): print(data["accounts"][i]["username"])
#     return data
# def add_exist_acc(username, password, filepath):
#     new_acc = {
#         "username": username,
#         "password": password
#     }
#     with open(filepath, "r") as f:
#         data = json.load(f)
#         data["accounts"].append(new_acc)
#     with open(filepath, "w") as f:
#         json.dump(data, f)
#     get_data(filepath)
# def login(username, password):
#     print(username)
#
#
# def input_validate(text):
#     text = text.lstrip()
#     return text.lower()
#
#
# def wait_command():
#     while True:
#         user_input = input("Write: ")
#         user_input = input_validate(user_input)
#         keys = user_input.split()
#         command = keys[0]
#         params = keys[1:len(keys)]
#         match command:
#             case "weather":
#                 weather(params)
#             case "exit":
#                 break
#             case _:
#                 continue




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
