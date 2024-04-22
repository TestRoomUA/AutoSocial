from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.types import Message, FSInputFile

from core.handlers.media import send_post
from core.keyboards.inline import start_inline_keyboard, main_keyboard
from core.utils.dbconnect import Request
from aiogram.utils.deep_linking import decode_payload
from core.settings import settings
from core.utils.objects import Post


async def get_start(message: Message, bot: Bot, counter: str, request: Request):
    await request.add_data(message.from_user.id, message.from_user.first_name)

    if counter == 1:
        start_message = f'Welcome, {message.from_user.first_name}!'
    else:
        start_message = f'Hello again, {message.from_user.first_name}!'

    photo = FSInputFile(fr'{settings.media.content}\hello.png')
    await bot.send_photo(message.chat.id, photo, caption=start_message, reply_markup=main_keyboard())


async def get_start_post(message: Message, bot: Bot, command: CommandObject, request: Request):
    start_message = f'Добро пожаловать, {message.from_user.first_name}, в наш цветочный уголок!'
    # photo = FSInputFile(fr'{settings.media.content}\start-photo.jpg')
    # await bot.send_photo(message.chat.id, photo, caption=start_message, reply_markup=start_inline_keyboard())
    #
    # args = command.args
    # payload = int(decode_payload(args))
    # data = await request.take_product_by_id(payload)
    # print(data)
    # page = data['rnum'] - 1
    # post = Post(db_id=payload,
    #             page=page,
    #             photos=data['photos'],
    #             title=data['name'],
    #             price=data['price'],
    #             count=data['count'])
    # await send_post(chat=message.chat.id, bot=bot, post=post, markup=market_product_keyboard(page))


async def get_photo(message: Message, bot: Bot):
    await message.answer(f'Thanks for image <tg-spoiler>...Downloading image...</tg-spoiler>')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, f'photo_{message.photo[-1].file_unique_id}.jpg')


async def get_message(message: Message, bot: Bot):
    try:
        await message.send_copy(chat_id=settings.bots.admin_id)
    except TypeError:
        await bot.send_message(chat_id=settings.bots.admin_id, text='Чтото не то -_-')

