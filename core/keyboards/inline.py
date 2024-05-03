import random
from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder


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
    keyboard_builder.button(text='Наш телеграм канал', url='https://t.me/+Xh2vMre6bmQ3MGU6')
    keyboard_builder.button(text='Вернутся в главное меню', callback_data='main')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(one_time_keyboard=True)


def market_start_keyboard(tags: List[str] | None = None):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='ХИТ СЕЗОНА', callback_data='post_create_0')
    if tags is not None:
        for tag in tags:
            keyboard_builder.button(text=f'{tag}', callback_data=f'post_create_0_{tag}')
    keyboard_builder.adjust(1, 2)
    return keyboard_builder.as_markup()


def market_product_keyboard(pageID: int, p_max: int, tag: str | None = None):
    keyboard_builder = InlineKeyboardBuilder()
    tag_str = ("_" + tag) if tag is not None else ""
    btns = 1
    if pageID > 0:
        btns += 1
        keyboard_builder.button(text='<', callback_data=f'post_edit_{pageID - 1}{tag_str}')
    keyboard_builder.button(text=f'({pageID + 1}/{p_max})', callback_data='current_page')
    if pageID < p_max - 1:
        btns += 1
        keyboard_builder.button(text='>', callback_data=f'post_edit_{pageID + 1}{tag_str}')
    keyboard_builder.button(text='Подробнее', callback_data=f'post_detailed_{pageID}{tag_str}')
    keyboard_builder.button(text='Выбрать категорию', callback_data='market')
    keyboard_builder.adjust(btns, 1)
    return keyboard_builder.as_markup()


def detailed_product_keyboard(pageID: int, tag: str | None = None):
    keyboard_builder = InlineKeyboardBuilder()
    tag_str = ("_" + tag) if tag is not None else ""
    keyboard_builder.button(text='Заказать с доставкой', callback_data=f'buy_{pageID}{tag_str}')
    keyboard_builder.button(text='< Вернутся к просмотру', callback_data=f'post_create_{pageID}{tag_str}')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def admin_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Посмотреть продукты', callback_data='admin_product_list')
    keyboard_builder.button(text='Добавить продукт', callback_data='admin_product_add')
    keyboard_builder.button(text='Удалить продукт', callback_data='admin_product_remove')
    keyboard_builder.button(text='Отправить новый пост на канал', callback_data='admin_post_channel')
    keyboard_builder.button(text='Выйти с панели админа', callback_data='admin_logout')
    keyboard_builder.adjust(1, 2, 1)
    return keyboard_builder.as_markup()


def product_test_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Заказать с доставкой', callback_data='test_product_buy')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def added_product(db_id: int):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Поделиться новостью на канале', callback_data=f'share_to_channel_{db_id}')
    keyboard_builder.button(text='Добавить ещё продукт', callback_data=f'admin_product_add')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def pay_keyboard(page: int, tag: str | None = None):
    keyboard_builder = InlineKeyboardBuilder()
    tag_str = ("_" + tag) if tag is not None else ''
    keyboard_builder.button(text='оплатить заказ с доставкой', pay=True)
    keyboard_builder.button(text='ccылка (пока нету)', url='https://google.com')
    keyboard_builder.button(text='< Вернутся', callback_data=f'post_create_{page}{tag_str}')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def channel_post_keyboard(link: str):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text=f"Перейти к боту {random.choice(['💐','🏵️','💮','🌸','🌹','🌺','🌻','🌼','🌷'])}", url=link)
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def channel_new_post_keyboard(text: str, link: str):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text=text, url=link)
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()