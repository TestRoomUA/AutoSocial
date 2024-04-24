from typing import List
from aiogram import Bot
# from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import Message, FSInputFile, InputMediaPhoto, InlineKeyboardMarkup, ReplyKeyboardMarkup
from core.settings import settings
from core.utils.objects import Post


async def send_post(chat: int, bot: Bot, post: Post, markup: InlineKeyboardMarkup | ReplyKeyboardMarkup = None, deleteMessages: List[int] = None):
    text = post_text(post.title, post.price, post.count)
    photos = post_photos(post.photos)
    await bot.send_photo(chat_id=chat, photo=photos[0], caption=text,
                         reply_markup=markup)
    for deleteMessage in deleteMessages:
        await bot.delete_message(chat_id=chat, message_id=deleteMessage)


async def edit_post(message: Message, bot: Bot, post: Post, markup: InlineKeyboardMarkup | ReplyKeyboardMarkup = None):
    text = post_text(post.title, post.price, post.count)
    media = post_medias(post.photos)
    await bot.edit_message_media(chat_id=message.chat.id, media=media[0], message_id=message.message_id)
    await bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id,
                                   caption=text, reply_markup=markup)


async def send_detailed_post(chat: int, bot: Bot, post: Post, markup: InlineKeyboardMarkup | ReplyKeyboardMarkup = None, deleteMessages: List[int] = None):
    text = post_text(post.title, post.price, post.price) + ('—' * 24)
    media = post_medias(post.photos)
    await bot.send_media_group(chat_id=chat, media=media)
    await bot.send_message(chat_id=chat, text=text, reply_markup=markup)
    for deleteMessage in deleteMessages:
        await bot.delete_message(chat_id=chat, message_id=deleteMessage)


def post_text(title: str, price: int, count: int):
    return f"<b>{title}</b>\r\nЦена: <i>{price} zł</i>\r\n{count} в наличии\r\n"


def post_photos(photos: List[str]):
    return [FSInputFile(fr"{settings.media.content}\{photo}") for photo in photos if photo not in ['None', None]]


def post_medias(photos: List[str]):
    return [InputMediaPhoto(type='photo', media=photo) for photo in post_photos(photos)]
