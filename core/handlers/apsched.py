from aiogram import Bot
from aiogram.types import FSInputFile
from core.settings import settings
from core.utils.objects import Post
from core.keyboards.inline import channel_post_keyboard
from aiogram.utils.deep_linking import create_start_link
from core.handlers.media import send_post


async def send_message_time(bot: Bot):
    await bot.send_message(settings.bots.admin_id, f'Send in a few seconds after Start')


async def send_message_cron(bot: Bot):
    await bot.send_message(settings.bots.admin_id, f'Send every day at the same time')


async def send_message_interval(bot: Bot):
    await bot.send_message(settings.bots.admin_id, f'Message with interval')


async def send_message_middleware(bot: Bot, chat_id: int):
    await bot.send_message(chat_id, f'middleware message~!')


async def send_news_products(bot: Bot, post_count: int):
    print(f"{post_count} : \r\n : {type(post_count)}")
    match post_count % 10:
        case 1:
            word = 'пост'
        case 2, 3, 4:
            word = 'поста'
        case _:
            word = 'постов'
    await bot.send_message(settings.channel.id, text=f'За эти 5 минут у вас: {post_count} {word}')


async def post_channel(bot: Bot, post: Post):
    link = await create_start_link(bot=bot, payload=str(post.db_id), encode=True)
    extra_text = '😎😎NEW😎😎'
    post.title = extra_text + '\r\n' + post.title
    await send_post(chat=settings.channel.id, bot=bot, post=post, markup=channel_post_keyboard(link))
