import asyncio
import json
import random
from typing import List

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from core.keyboards.inline import added_product, channel_post_keyboard, channel_new_post_keyboard
from core.utils.dbconnect import Request
from core.utils.objects import Post
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.handlers.media import send_post_channel
from aiogram.utils.deep_linking import create_start_link
from datetime import datetime, timedelta, timezone
from core.settings import settings


async def send_new_product(call: CallbackQuery, bot: Bot, request: Request):
    context_data = call.data.split('_')
    db_id = int(context_data[3])
    link = await create_start_link(bot=bot, payload=str(db_id), encode=True)
    post_data = await request.take_product_by_id(db_id)

    result = await request.take_file_ids(post_data['content_ids'])
    file_ids = [(file_id if isinstance(file_id, int) else file_id['file_id']) for file_id in result]
    page = post_data['rnum'] - 1
    post = Post(
        title=post_data['name'],
        price=post_data['price'],
        count=post_data['count'],
        file_ids=file_ids,
        page=page,
        db_id=post_data['id'],
        desc=post_data['description'],
        tags=post_data['tags']
    )
    extra_text = '😎😎NEW😎😎'
    post.title = extra_text + '\r\n' + post.title
    await send_post_channel(chat=settings.channel.id, bot=bot, post=post, markup=channel_post_keyboard(link))


async def send_post_to_channel(chat: str, bot: Bot, text: str, photo_file_id: str | None = None, video_file_id: str | None = None, btn_text: str | None = None, btn_link: str | None = None):
    if photo_file_id is not None:
        await bot.send_photo(chat_id=chat, photo=photo_file_id, caption=text, reply_markup=channel_new_post_keyboard(btn_text, btn_link))
    elif video_file_id is not None:
        await bot.send_video(chat_id=chat, video=video_file_id, caption=text, reply_markup=channel_new_post_keyboard(btn_text, btn_link))
    else:
        await bot.send_message(chat_id=chat, text=text, reply_markup=channel_new_post_keyboard(btn_text, btn_link))