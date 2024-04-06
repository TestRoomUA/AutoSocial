from aiogram import Bot
from core.settings import settings


async def send_message_time(bot: Bot):
    await bot.send_message(settings.bots.admin_id, f'Send in a few seconds after Start')


async def send_message_cron(bot: Bot):
    await bot.send_message(settings.bots.admin_id, f'Send every day at the same time')


async def send_message_interval(bot: Bot):
    await bot.send_message(settings.bots.admin_id, f'Message with interval')


async def send_message_middleware(bot: Bot, chat_id: int):
    await bot.send_message(chat_id, f'middleware message~!')