from aiogram import Bot
from aiogram.types import CallbackQuery
from core.utils.callbackdata import CarInfo
from core.keyboards.reply import get_data_reply_keyboard
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


async def select_car(call: CallbackQuery, bot: Bot, callback_data: CarInfo):
    brand = callback_data.brand
    model = callback_data.model
    color = callback_data.color
    year = callback_data.year
    answer = f'{call.from_user.first_name}, you chose car {brand} model {model} color {color.capitalize()} and year {year}'
    await call.message.answer(answer)
    await call.answer()
    json_str = json.dumps(call.dict(), default=str, indent=4)
    print(json_str)


async def select_start(call: CallbackQuery, bot: Bot):
    data = call.data
    match data:
        case 'start_private_data':
            await call.message.answer(f'Мне нужен твой телефон, геолокация и возраст', reply_markup=get_data_reply_keyboard())
            await call.answer()
        case 'start_market':
            pass
        case 'start_saver':
            pass
