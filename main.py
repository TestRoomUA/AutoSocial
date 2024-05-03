# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from aiogram import Bot, Dispatcher, F
from aiogram.types import ContentType
from aiogram.fsm.storage.memory import MemoryStorage
from core.handlers.basic import get_start, get_start_deep_link, get_message, contacts_info
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio
import logging
from core.settings import settings
from aiogram.filters import Command, CommandStart
from core.utils.commands import set_commands
from core.handlers.callback import contacts_info_call, send_contact_data, get_main_menu
from core.handlers.pay import order, pre_checkout_query, successful_payment, shipping_check
from core.middlewares.countermiddleware import CounterMiddleware
from core.middlewares.officehours import OfficeHoursMiddleware
from core.middlewares.dbmiddleware import DbSession
from core.middlewares.apschedulermiddleware import SchedulerMiddleware
from core.middlewares.guestmiddleware import GuestCounterMiddleware
# import psycopg_pool
import asyncpg
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.handlers import apsched
from datetime import datetime, timedelta
from core.handlers.market import market_open, market_call, show_post_call
from core.handlers.admin import admin_mode, admin_callback, \
    add_product_photo_group, add_product_name, add_product_price, add_product_description, add_product_tags, add_product_quantity, add_product_check_successful, add_product_check_fail, \
    button_next_added_product_photo, create_post, create_post_button
from core.utils.states import AdminState, AdminPanelState
from core.utils.debugger import test_button
from aiogram.utils.chat_action import ChatActionMiddleware
from core.middlewares.example_chat_action_middleware import ExampleChatActionMiddleware
from core.middlewares.jsonmiddleware import JsonMiddleware, JsonCallMiddleware
from core.middlewares.albummiddleware import AlbumMiddleware
from core.handlers.channel import send_new_product
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Bot started!', disable_notification=True)


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Bot stopped', disable_notification=True)


async def create_pool():  # async
    # return psycopg_pool.AsyncConnectionPool(f"host='localhost' port=5433 dbname=postgres user=postgres password=pCJbF34siSwvLgmevBL9 "
    #                                         f"connect_timeout=60")
    return await asyncpg.create_pool(user='postgres',
                                     host='localhost',
                                     password='pCJbF34siSwvLgmevBL9',
                                     database='postgres',
                                     port=5433,
                                     command_timeout=60)


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                                "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )
    storage = MemoryStorage()
    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    pool_connect = await create_pool()
    dp = Dispatcher(storage=storage)
    scheduler = AsyncIOScheduler(timezone="Europe/Warsaw")
    # scheduler.add_job(apsched.send_message_time, trigger='date', run_date=datetime.now() + timedelta(seconds=10),
    #                   kwargs={'bot': bot})
    # scheduler.add_job(apsched.send_message_cron, trigger='cron', hour=datetime.now().hour, minute=datetime.now().minute + 1,
    #                   start_date=datetime.now(), kwargs={'bot': bot})
    # scheduler.add_job(apsched.send_news_products, trigger='interval', seconds=30, kwargs={'bot': bot, 'post_count': 1})
    scheduler.start()

    dp.update.middleware.register(DbSession(pool_connect))
    dp.message.middleware.register(AlbumMiddleware())
    dp.message.middleware.register(CounterMiddleware())
    dp.message.middleware.register(GuestCounterMiddleware())
    dp.message.middleware.register(OfficeHoursMiddleware())  # dp.update
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    dp.update.middleware.register(ExampleChatActionMiddleware())
    dp.message.middleware.register(JsonMiddleware())
    dp.callback_query.middleware.register(JsonCallMiddleware())
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.callback_query.register(show_post_call, F.data.startswith('post_'), flags={'chat_action': 'upload_photo'})
    dp.callback_query.register(order, F.data.startswith('buy_'), flags={'chat_action': 'typing'})
    dp.callback_query.register(test_button, F.data == 'test_product_buy')
    dp.callback_query.register(send_new_product, F.data.startswith('share_'))
    dp.callback_query.register(get_main_menu, F.data == 'main')

    dp.message.register(contacts_info, Command(commands=['contact']))
    dp.callback_query.register(contacts_info_call, F.data == 'contacts')

    dp.message.register(market_open, Command(commands=['market']))
    dp.callback_query.register(market_call, F.data.startswith('market'))

    dp.message.register(create_post, F.text, AdminState.CREATE_POST)
    dp.message.register(create_post_button, F.text, AdminState.CREATE_POST_BUTTON)
    dp.message.register(add_product_photo_group, F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO, ContentType.DOCUMENT]), AdminState.ADD_PRODUCT)
    dp.message.register(button_next_added_product_photo, F.text.lower() == 'далее', AdminState.ADD_PRODUCT)
    dp.message.register(add_product_name, F.text, AdminState.ADDED_PRODUCT_PHOTO)
    dp.message.register(add_product_price, F.text, AdminState.ADDED_PRODUCT_NAME)
    dp.message.register(add_product_description, F.text, AdminState.ADDED_PRODUCT_PRICE)
    dp.message.register(add_product_tags, F.text, AdminState.ADDED_PRODUCT_DESC)
    dp.message.register(add_product_quantity, F.text, AdminState.ADDED_PRODUCT_TAGS, flags={'chat_action': 'upload_photo'})
    dp.message.register(add_product_check_successful, F.text.lower() == 'далее', AdminState.ADDED_PRODUCT_CHECK)
    dp.message.register(add_product_check_fail, F.text, AdminState.ADDED_PRODUCT_CHECK)
    dp.pre_checkout_query.register(pre_checkout_query)
    dp.message.register(successful_payment, F.content_type == ContentType.SUCCESSFUL_PAYMENT)
    dp.shipping_query.register(shipping_check)
    dp.callback_query.register(send_contact_data, F.data.startswith('contacts_'))
    dp.message.register(get_start_deep_link, CommandStart(deep_link=True), flags={'chat_action': 'typing'})
    dp.message.register(get_start, CommandStart(), flags={'chat_action': 'typing'})
    dp.callback_query.register(admin_callback, AdminPanelState.ADMIN)
    dp.message.register(admin_mode, Command(commands=['admin']), F.from_user.id == settings.bots.admin_id)
    dp.message.register(get_message)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
