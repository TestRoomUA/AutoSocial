from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.callbackdata import ProductInfo, ProductID


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


# def get_inline_keyboard():
#     keyboard_builder = InlineKeyboardBuilder()
#     keyboard_builder.button(text='Toyota Camry Red 2021', callback_data=CarInfo(
#         brand='Toyota', model='Camry', color='red', year=2021
#     ))
#     keyboard_builder.button(text='Toyota Corolla Gray 2017', callback_data=CarInfo(
#         brand='Toyota', model='Corolla', color='gray', year=2017
#     ))
#     keyboard_builder.button(text='Nissan GTR White 2019', callback_data=CarInfo(
#         brand='Nissan', model='GTR', color='white', year=2019
#     ))
#     keyboard_builder.button(text='Youtube', url='https://www.youtube.com/playlist?list=PLRU2Gs7fnCuiwcEDU0AWGkSTawEQpLFPb')
#     keyboard_builder.button(text='Telegram', url='tg://user?id=814140059')
#     keyboard_builder.adjust(3)
#     return keyboard_builder.as_markup()


def start_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Цветы', callback_data='market')
    keyboard_builder.button(text='Контакты', callback_data='contacts')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def contacts_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Номер телефона", callback_data='contacts_phone')
    keyboard_builder.button(text='Наша точка', url='https://maps.app.goo.gl/hWprhs6bS8NCAGM5A')
    keyboard_builder.button(text='Наш телеграм канал', url='tg://user?id=814140059')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def market_start_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='ХИТ СЕЗОНА', callback_data='post_0')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def market_product_keyboard(pageID: int):
    keyboard_builder = InlineKeyboardBuilder()
    if pageID > 0:
        keyboard_builder.button(text='<', callback_data=f'post_{pageID - 1}')
    keyboard_builder.button(text=f'({pageID + 1})', callback_data='current_page')
    keyboard_builder.button(text='>', callback_data=f'post_{pageID + 1}')
    keyboard_builder.button(text='Подробнее', callback_data=f'detailed_{pageID}')
    if pageID > 0:
        keyboard_builder.adjust(3, 1)
    else:
        keyboard_builder.adjust(2, 1)
    return keyboard_builder.as_markup()


def detailed_product_keyboard(productID: int):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Заказать с доставкой', callback_data=f'buy_{productID}')
    keyboard_builder.button(text='Вернутся к просмотру', callback_data=f'post_{productID}')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def admin_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Посмотреть продукты', callback_data='admin_product_list')
    keyboard_builder.button(text='Добавить продукт', callback_data='admin_product_add')
    keyboard_builder.button(text='Удалить продукт', callback_data='admin_product_remove')
    keyboard_builder.button(text='Выйти с панели админа', callback_data='admin_logout')
    keyboard_builder.adjust(1, 2, 1)
    return keyboard_builder.as_markup()


def product_test_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Заказать с доставкой', callback_data='test_product_buy')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def channel_post_keyboard(link: str):
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text='Перейти к боту', url=link)
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()