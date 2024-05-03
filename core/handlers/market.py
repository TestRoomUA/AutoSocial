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


async def market_open(message: Message | CallbackQuery, bot: Bot, request: Request):
    photo = FSInputFile(fr'{settings.media.content}\market.jpeg')
    req = await request.take_all_tags()
    print(req)
    nl = '\r\n'
    text = f'Ось наша витрина, выбирай категорию или нажми кнопку "ХИТ СЕЗОНА"\r\n'
    # \r\n{f", {nl}".join("<code>#" + tag + "</code>" for tag in req["all_tags"])}
    markup = market_start_keyboard(tags=req["all_tags"])
    chat = message.chat.id
    await bot.delete_message(chat_id=chat, message_id=message.message_id)
    await bot.send_photo(chat_id=chat, photo=photo,
                         caption=text, reply_markup=markup)


async def market_call(call: CallbackQuery, bot: Bot, request: Request):
    await market_open(message=call.message, bot=bot, request=request)
    await call.answer()


async def show_post(bot: Bot, request: Request, chat_id: int, message_id: int, command: str, page: int, tag: str | None = None):
    post_data = await request.take_product(page, tag)
    req_max = await request.take_product_count(tag)
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

    match command:
        case 'edit':
            await edit_post(chat=chat_id, message_id=message_id, bot=bot, post=post, markup=market_product_keyboard(page, row_max, tag))
        case 'create':
            await send_post(chat=chat_id, bot=bot, post=post, markup=market_product_keyboard(page, row_max, tag), deleteMessages=[message_id])
        case 'detailed':
            await send_detailed_post(chat=chat_id, bot=bot, post=post, markup=detailed_product_keyboard(page, tag), deleteMessages=[message_id])


async def show_post_call(call: CallbackQuery, bot: Bot, request: Request):
    data = call.data.split('_')
    command = data[1]
    page = int(data[2])
    tag = data[3] if len(data) > 3 else None
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await show_post(bot=bot, request=request, command=command, page=page, tag=tag, chat_id=chat_id, message_id=message_id)
    await call.answer()

