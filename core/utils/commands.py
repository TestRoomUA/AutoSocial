from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Start work'
        ),
        # BotCommand(
        #     command='help',
        #     description='HELP, all functions'
        # ),
        BotCommand(
            command='contact',
            description='Our contacts'
        ),
        BotCommand(
            command='market',
            description='flower market'
        ),
        BotCommand(
            command='admin',
            description='Панель хозяина'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
