from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from core.handlers.basic import get_start, get_start_post, get_message
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio
import logging
from core.settings import settings
from aiogram.filters import Command, CommandStart
from core.utils.commands import set_commands
from core.middlewares.countermiddleware import CounterMiddleware
from core.middlewares.officehours import OfficeHoursMiddleware
from core.middlewares.dbmiddleware import DbSession
from core.middlewares.apschedulermiddleware import SchedulerMiddleware
import asyncpg
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.handlers import apsched
from datetime import datetime, timedelta
from core.handlers.admin import admin_mode, admin_callback
from core.utils.statesform import AdminPanelState
from aiogram.utils.chat_action import ChatActionMiddleware
from core.middlewares.example_chat_action_middleware import ExampleChatActionMiddleware
from core.middlewares.jsonmiddleware import JsonMiddleware
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Bot started!')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Bot stopped')


async def create_pool():
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
    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    pool_connect = await create_pool()
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone="Europe/Warsaw")
    # scheduler.add_job(apsched.send_message_time, trigger='date', run_date=datetime.now() + timedelta(seconds=10),
    #                   kwargs={'bot': bot})
    # scheduler.add_job(apsched.send_message_cron, trigger='cron', hour=datetime.now().hour, minute=datetime.now().minute + 1,
    #                   start_date=datetime.now(), kwargs={'bot': bot})
    # scheduler.add_job(apsched.send_news_products, trigger='interval', seconds=30, kwargs={'bot': bot, 'post_count': 1})
    scheduler.start()

    dp.update.middleware.register(DbSession(pool_connect))
    dp.message.middleware.register(CounterMiddleware())
    # dp.message.middleware.register(CommandMiddleware())
    dp.message.middleware.register(OfficeHoursMiddleware())  # dp.update
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    dp.update.middleware.register(ExampleChatActionMiddleware())
    dp.message.middleware.register(JsonMiddleware())
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(get_start_post, CommandStart(deep_link=True), flags={'chat_action': 'typing'})
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
