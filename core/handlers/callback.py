from aiogram import Bot
from aiogram.types import CallbackQuery
from core.utils.callbackdata import ProductInfo
from core.keyboards.reply import get_data_reply_keyboard
from core.keyboards.inline import contacts_inline_keyboard
import json


# async def select_car(call: CallbackQuery, bot: Bot):
#     arr = call.data.split('_')
#
#     brand = arr[0]
#     model = arr[1]
#     color = arr[2]
#     year = arr[3]
#     answer = f'{call.from_user.first_name}, you chose car {brand.capitalize()} model {model.capitalize()} color {color.capitalize()} and year {year}'
#     await call.message.answer(answer)
#     await call.answer()
#     json_str = json.dumps(call.dict(), default=str, indent=4)
#     print(json_str)


# async def select_product(call: CallbackQuery, bot: Bot, callback_data: ProductInfo):
#     name = callback_data.name
#     description = callback_data.description
#     color = callback_data.color
#     price = callback_data.price
#     in_stock = callback_data.inStock
#
#     answer = f'{call.from_user.first_name}, you chose product {brand} model {model} color {color.capitalize()} and year {year}'
#     await call.message.answer(answer)
#     await call.answer()
#     json_str = json.dumps(call.dict(), default=str, indent=4)
#     print(json_str)


async def contacts_info(call: CallbackQuery, bot: Bot):
    await call.message.answer_location(latitude=52.22885316035805, longitude=21.003265512062914, reply_markup=contacts_inline_keyboard())
    await call.answer()
    json_str = json.dumps(call.dict(), default=str, indent=4)
    print(json_str)


async def send_contact_data(call: CallbackQuery, bot: Bot):
    data = call.data
    match data:
        case 'contacts_phone':
            await call.message.answer_contact(phone_number='+1234567890', first_name='Цветочный', last_name='уголок')
        case 'contacts_location':
            await call.message.answer_location(latitude=52.22885316035805, longitude=21.003265512062914)
    await call.answer()


async def select_start(call: CallbackQuery, bot: Bot):
    data = call.data
    match data:
        case 'start_private_data':
            await call.message.answer(f'Мне нужен твой телефон, геолокация и возраст', reply_markup=get_data_reply_keyboard())
    await call.answer()
