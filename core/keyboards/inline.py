from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Цветы', callback_data='market')
    keyboard_builder.button(text='Контакты', callback_data='contacts')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def main_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='New POST', callback_data='admin_post')
    keyboard_builder.button(text='New CHANNEL', callback_data='admin_channel')
    keyboard_builder.button(text='Posts in queue', callback_data='admin_product_remove')
    keyboard_builder.button(text='List of channels', callback_data='admin_logout')
    keyboard_builder.adjust(2, 2, 1)
    return keyboard_builder.as_markup()


def channel_post_keyboard(buttons: List[str, str]):
    keyboard_builder = InlineKeyboardBuilder()
    for text, link in buttons:
        keyboard_builder.button(text=text, url=link)
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
