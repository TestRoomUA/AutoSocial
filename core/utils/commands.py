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
            command='save',
            description='save reply stickers, GIFs, photos, videos, voice...'
        ),
        # BotCommand(
        #     command='info',
        #     description='all bot info'
        # ),
        BotCommand(
            command='hello',
            description='Say Hello to me'
        ),
        BotCommand(
            command='inline',
            description='Show inline buttons'
        ),
        BotCommand(
            command='pay',
            description='test payment'
        ),
        BotCommand(
            command='form',
            description='little form'
        ),
        BotCommand(
            command='audio',
            description='Bot send audio'
        ),
        BotCommand(
            command='document',
            description='Bot send document'
        ),
        BotCommand(
            command='photo',
            description='Bot send photo'
        ),
        BotCommand(
            command='video',
            description='Bot send video'
        ),
        BotCommand(
            command='video_note',
            description='Bot send video note'
        ),
        BotCommand(
            command='voice',
            description='Bot send voice'
        ),
        BotCommand(
            command='mediagroup',
            description='Bot send group of media'
        ),
        BotCommand(
            command='sticker',
            description='Bot send sticker'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
