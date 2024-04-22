from typing import List
from aiogram import Bot
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto, InlineKeyboardMarkup, ReplyKeyboardMarkup

from core.settings import settings
from core.utils.objects import Post


def get_media(media: List[str], caption: str, reply: InlineKeyboardMarkup):
    group_builder = MediaGroupBuilder(caption=caption)
    for i, media_item in enumerate(media):
        group_builder.add(type='photo', media=FSInputFile(media_item))
    return group_builder.build()


async def send_post(chat: int, bot: Bot, post: Post, markup: InlineKeyboardMarkup | ReplyKeyboardMarkup = None):
    text = post_text(post.title, post.price, post.count)
    photos = post_photos(post.photos)
    markup = post_markup(markup)
    await bot.send_photo(chat_id=chat, photo=photos[0], caption=text,
                         reply_markup=markup)


async def edit_post(message: Message, bot: Bot, post: Post, markup: InlineKeyboardMarkup | ReplyKeyboardMarkup = None):
    text = post_text(post.title, post.price, post.count)
    media = post_medias(post.photos)
    markup = post_markup(markup)
    await bot.edit_message_media(chat_id=message.chat.id, media=media[0], message_id=message.message_id)
    await bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id,
                                   caption=text, reply_markup=markup)


def post_text(title: str, price: int, count: int):
    return f"<b>{title}</b>\r\nЦена: <i>{price} zł</i>\r\n{count} в наличии"


def post_photos(photos: List[str]):
    return [FSInputFile(fr"{settings.media.content}\{photo}") for photo in photos if photo not in ['None', None]]


def post_medias(photos: List[str]):
    return [InputMediaPhoto(type='photo', media=photo) for photo in post_photos(photos)]


def post_markup(markup: InlineKeyboardMarkup | ReplyKeyboardMarkup):
    return markup
