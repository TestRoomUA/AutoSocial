from typing import List
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto, InlineKeyboardMarkup


def get_media(media: List[str], caption: str, reply: InlineKeyboardMarkup):
    group_builder = MediaGroupBuilder(caption=caption)
    for i, media_item in enumerate(media):
        group_builder.add(type='photo', media=FSInputFile(media_item))
    return group_builder.build()
