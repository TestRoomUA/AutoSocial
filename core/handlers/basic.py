import pytz
from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.types import Message, FSInputFile, CallbackQuery
from datetime import datetime, timezone
from core.handlers.market import show_post
from core.handlers.media import send_post
from core.keyboards.inline import start_inline_keyboard, contacts_inline_keyboard, market_product_keyboard
from core.utils.dbconnect import Request
from aiogram.utils.deep_linking import decode_payload
from core.settings import settings
from core.utils.objects import Post


def get_now():
    return datetime.now(timezone.utc)


async def get_start(message: Message, bot: Bot, counter: str, request: Request):
    date = get_now()
    username = message.from_user.first_name.replace("'", "").replace('"', '')
    await request.add_userdata(message.from_user.id, username, date)

    if counter == 1:
        start_message = f'Добро пожаловать, {message.from_user.first_name}, в наш цветочный уголок!'
    else:
        start_message = f'Снова привет, {message.from_user.first_name}!'

    photo = FSInputFile(fr'{settings.media.content}\start-photo.jpg')
    await bot.send_photo(message.chat.id, photo, caption=start_message, reply_markup=start_inline_keyboard())


async def get_start_deep_link(message: Message, bot: Bot, counter: str, command: CommandObject, request: Request):
    await get_start(message=message, bot=bot, counter=counter, request=request)

    args = command.args
    try:
        payload: str = decode_payload(args)
    except UnicodeDecodeError as e:
        print(e)
        payload: str = args
    if payload.startswith('from_'):
        match payload.split('_')[1]:
            case 'channel':
                return

    post_id = int(payload)
    data = await request.take_product_by_id(post_id)
    page = data['rnum'] - 1
    await show_post(bot=bot, request=request, chat_id=message.chat.id, message_id=message.message_id, command='create', page=page)


async def get_photo(message: Message, bot: Bot):
    await message.answer(f'Thanks for image <tg-spoiler>...Downloading image...</tg-spoiler>')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, f'photo_{message.photo[-1].file_unique_id}.jpg')


async def get_sticker(message: Message, bot: Bot):
    await message.answer(f'Thanks for sticker <tg-spoiler>...Downloading...</tg-spoiler>')

    file = await bot.get_file(message.sticker.file_id)
    if message.sticker.is_video or message.sticker.is_animated:
        await bot.download_file(file.file_path, f'sticker-video-{message.sticker.file_unique_id}.mp4')
    else:
        await bot.download_file(file.file_path, f'sticker-image-{message.sticker.file_unique_id}.jpg')
    await message.reply(f'Done!')


async def get_voice(message: Message, bot: Bot):
    await message.answer(f'Wow nice voice! <tg-spoiler>...Downloading...</tg-spoiler>')
    file = await bot.get_file(message.voice.file_id)
    await bot.download_file(file.file_path, f'voice-{message.voice.file_unique_id}.wav')


async def get_message(message: Message, bot: Bot):
    if message.from_user.id == settings.bots.admin_id:
        return
    try:
        await message.send_copy(chat_id=settings.bots.admin_id)
    except TypeError:
        await bot.send_message(chat_id=settings.bots.admin_id, text='Чтото не то -_-')


async def contacts_info(message: Message | CallbackQuery, bot: Bot):
    if isinstance(message, Message):
        chat = message.chat.id
    else:
        chat = message.message.chat.id
    markup = contacts_inline_keyboard()
    await bot.send_location(chat_id=chat, latitude=52.22885316035805, longitude=21.003265512062914, reply_markup=markup)
