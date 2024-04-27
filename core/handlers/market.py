from typing import List
from aiogram import Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from core.keyboards.inline import market_product_keyboard, market_start_keyboard, detailed_product_keyboard
from aiogram.methods.delete_message import DeleteMessage
from core.utils.dbconnect import Request
from core.utils.objects import Post
from core.handlers.media import edit_post, send_post, send_detailed_post
from core.settings import settings


async def market_open(message: Message | CallbackQuery, bot: Bot):
    photo = FSInputFile(fr'{settings.media.content}\market.jpeg')
    text = f'Ось наша витрина, выбирай категорию или нажми кнопку "ХИТ СЕЗОНА"\r\n\r\n*категорий пока нет:(*'
    markup = market_start_keyboard()
    if isinstance(message, CallbackQuery):
        call = message
        chat = call.message.chat.id
        msg_id = call.message.message_id
        media = InputMediaPhoto(type='photo', media=photo)
        await bot.edit_message_media(chat_id=chat, media=media, message_id=msg_id)
        await bot.edit_message_caption(chat_id=chat, message_id=msg_id, caption=text, reply_markup=markup)
        await call.answer()
    elif isinstance(message, Message):
        await bot.send_photo(chat_id=message.chat.id, photo=photo,
                             caption=text, reply_markup=markup)
    else:
        pass


async def market_call(call: CallbackQuery, bot: Bot):
    await market_open(message=call, bot=bot)


async def show_post(call: CallbackQuery, bot: Bot, request: Request):
    data = call.data.split('_')
    page = int(data[2])
    post_data = await request.take_product(page)
    req_max = await request.take_product_count()
    row_max = req_max['r_max']

    result = await request.take_file_ids(post_data['content_ids'])
    file_ids = [(file_id if isinstance(file_id, int) else file_id['file_id']) for file_id in result]

    post = Post(title=post_data['name'],
                price=post_data['price'],
                count=post_data['count'],
                file_ids=file_ids,
                page=page,
                db_id=post_data['id'],
                desc=post_data['description'],
                tags=post_data['tags'])
    chat_id = call.message.chat.id
    match data[1]:
        case 'edit':
            await edit_post(message=call.message, bot=bot, post=post, markup=market_product_keyboard(page, row_max))
        case 'create':
            await send_post(chat=chat_id, bot=bot, post=post, markup=market_product_keyboard(page, row_max), deleteMessages=[call.message.message_id])
        case 'detailed':
            await send_detailed_post(chat=chat_id, bot=bot, post=post, markup=detailed_product_keyboard(page), deleteMessages=[call.message.message_id])
    await call.answer()
