from aiogram import Bot
from aiogram.types import CallbackQuery
from core.keyboards.reply import get_data_reply_keyboard
from core.keyboards.inline import contacts_inline_keyboard
from core.handlers.basic import contacts_info


async def contacts_info_call(call: CallbackQuery, bot: Bot):
    await contacts_info(message=call, bot=bot)
    await call.answer()


async def send_contact_data(call: CallbackQuery, bot: Bot):
    data = call.data
    match data:
        case 'contacts_phone':
            await call.message.answer_contact(phone_number='+1234567890', first_name='Цветочный', last_name='уголок')
        case 'contacts_location':
            await bot.send_location(chat_id=call.message.id, latitude=52.22885316035805, longitude=21.003265512062914)
    await call.answer()


async def select_start(call: CallbackQuery, bot: Bot):
    data = call.data
    match data:
        case 'start_private_data':
            await call.message.answer(f'Мне нужен твой телефон, геолокация и возраст', reply_markup=get_data_reply_keyboard())
    await call.answer()
