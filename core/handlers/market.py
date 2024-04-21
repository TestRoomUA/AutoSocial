import asyncio
import json
from typing import List

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from core.keyboards.inline import market_product_keyboard, market_start_keyboard, detailed_product_keyboard
from core.utils.callbackdata import ProductInfo, ProductID
from aiogram.fsm.context import FSMContext
from aiogram.methods.delete_message import DeleteMessage
from core.utils.dbconnect import Request
from core.utils.objects import Post
from core.utils.statesform import ChatState
from core.handlers.media import edit_post, send_post
from core.settings import settings


async def market_command(message: Message, bot: Bot):
    photo = FSInputFile(fr'{settings.media.content}\market.jpeg')
    text = f'Ось наша витрина, выбирай категорию или нажми кнопку "ХИТ СЕЗОНА"\r\n\r\n*категорий пока нет:(*'
    await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text,
                         reply_markup=market_start_keyboard())


async def market_call(call: CallbackQuery, bot: Bot):
    photo = InputMediaPhoto(type='photo', media=FSInputFile(fr"{settings.media.content}\market.jpeg"))
    text = f'Ось наша витрина, выбирай категорию или нажми кнопку "ХИТ СЕЗОНА"\r\n\r\n*категорий пока нет:(*'
    await bot.edit_message_media(chat_id=call.message.chat.id, media=photo, message_id=call.message.message_id)
    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   caption=text,
                                   reply_markup=market_start_keyboard())
    await call.answer()


async def show_post_by_index(call: CallbackQuery, bot: Bot, request: Request):
    data = call.data.split('_')
    page = int(data[1])
    post_data = await request.take_product(page)
    name = post_data['name']
    price = post_data['price']
    count = post_data['count']
    photos = post_data['photos']
    db_id = post_data['id']
    post = Post(title=name,
                price=price,
                count=count,
                photos=photos,
                page=page,
                db_id=db_id)
    await edit_post(bot=bot, message=call.message, post=post, markup=market_product_keyboard(page))
    await call.answer()


async def show_detailed_post(call: CallbackQuery, bot: Bot, request: Request):
    data = call.data.split('_')
    index = int(data[1])
    post_data = await request.take_product(index)
    name = post_data['name']
    price = post_data['price']
    count = post_data['count']
    photos: List[str] = post_data['photos']
    text = f"{name}\r\n Цена: {price} zł\r\n{count} в букете"

    media = [InputMediaPhoto(type='photo', media=FSInputFile(fr"{settings.media.content}\{photo}"))for photo in photos if photo not in [None, 'None']]
    media[0].caption = text
    await bot.send_media_group(chat_id=call.message.chat.id, media=media)

    await bot.send_message(chat_id=call.message.chat.id,
                           text=text,
                           reply_markup=detailed_product_keyboard(index))
    delete = DeleteMessage(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await bot(delete)
    await call.answer()
