from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.callbackdata import CarInfo

select_car = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Toyota Camry Red 2021',
            callback_data='toyota_camry_red_2021'
        )
    ],
    [
        InlineKeyboardButton(
            text='Toyota Corolla Gray 2017',
            callback_data='toyota_corolla_gray_2017'
        )
    ],
    [
        InlineKeyboardButton(
            text='Nissan GTR White 2019',
            callback_data='nissan_gtr_white_2019'
        )
    ],
    [
        InlineKeyboardButton(
            text='Youtube',
            url='https://www.youtube.com/watch?v=XJCYxIbsXmk&list=PLRU2Gs7fnCuiwcEDU0AWGkSTawEQpLFPb&index=6&ab_channel=NZTCODER'
        )
    ],
    [
        InlineKeyboardButton(
            text='telegram',
            url='tg://user?id=1461211665'
        )
    ]
])


def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Toyota Camry Red 2021', callback_data=CarInfo(
        brand='Toyota', model='Camry', color='red', year=2021
    ))
    keyboard_builder.button(text='Toyota Corolla Gray 2017', callback_data=CarInfo(
        brand='Toyota', model='Corolla', color='gray', year=2017
    ))
    keyboard_builder.button(text='Nissan GTR White 2019', callback_data=CarInfo(
        brand='Nissan', model='GTR', color='white', year=2019
    ))
    keyboard_builder.button(text='Youtube', url='https://www.youtube.com/playlist?list=PLRU2Gs7fnCuiwcEDU0AWGkSTawEQpLFPb')
    keyboard_builder.button(text='Telegram', url='tg://user?id=814140059')
    keyboard_builder.adjust(3)
    return keyboard_builder.as_markup()


def start_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Поделись со мной своими данными:)', callback_data='start_private_data')
    keyboard_builder.button(text='РОЗПРОДАЖА', callback_data='start_market')
    keyboard_builder.button(text='Сохранялка', callback_data='start_saver')
    keyboard_builder.button(text='Youtube', url='https://www.youtube.com/playlist?list=PLRU2Gs7fnCuiwcEDU0AWGkSTawEQpLFPb')
    keyboard_builder.button(text='Telegram', url='tg://user?id=814140059')
    keyboard_builder.adjust(1, 2)
    return keyboard_builder.as_markup()
