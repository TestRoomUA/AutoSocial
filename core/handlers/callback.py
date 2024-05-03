from aiogram import Bot
from aiogram.types import CallbackQuery
from core.keyboards.reply import get_data_reply_keyboard
from core.keyboards.inline import contacts_inline_keyboard, start_inline_keyboard
from core.handlers.basic import contacts_info


async def get_main_menu(call: CallbackQuery, bot: Bot):
    main_message = f'Вы в главном меню'
    photo = 'AgACAgIAAxkBAAIGoWYubQhrlEPi-7K4ITfGyg0YemapAAJI2TEbSmJ4SXJSC-8mTCobAQADAgADeAADNAQ'
    chat = call.message.chat.id
    msg_id = call.message.message_id
    await bot.send_photo(chat_id=chat, photo=photo, caption=main_message, reply_markup=start_inline_keyboard())
    await bot.delete_message(chat_id=chat, message_id=msg_id)


async def contacts_info_call(call: CallbackQuery, bot: Bot):
    await contacts_info(message=call.message, bot=bot)
    await call.answer()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


async def send_contact_data(call: CallbackQuery, bot: Bot):
    data = call.data
    match data:
        case 'contacts_phone':
            await call.message.answer_contact(phone_number='+1234567890', first_name='Цветочный', last_name='уголок')
        case 'contacts_location':
            await bot.send_location(chat_id=call.message.id, latitude=52.22885316035805, longitude=21.003265512062914)
    await call.answer()
