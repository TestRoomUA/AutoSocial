from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

loc_tel_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Send your location',
            request_location=True
        )
    ],
    [
        KeyboardButton(
            text='Send your phone number',
            request_contact=True
        )
    ],
    [
        KeyboardButton(
            text='Create Quiz',
            request_poll=KeyboardButtonPollType(type='quiz')
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Send location, phone number or create a quiz ↓ ')


def get_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Geolocation', request_location=True)
    keyboard_builder.button(text='Phone number', request_contact=True)
    keyboard_builder.button(text='QUIZ', request_poll=KeyboardButtonPollType(type='quiz'))
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Send location, phone number or create a quiz ↓')


def get_data_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Геолокация', request_location=True)
    keyboard_builder.button(text='Номер телефона', request_contact=True)
    keyboard_builder.button(text='Анкета')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def admin_add_photo_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Далее')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Отправьте ещё фото, либо нажмите кнопку 'Далее'")