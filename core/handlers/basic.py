from aiogram import Bot
from aiogram.types import Message, FSInputFile
from core.keyboards.inline import start_inline_keyboard, contacts_inline_keyboard
from core.utils.dbconnect import Request
from core.settings import settings


async def get_start(message: Message, bot: Bot, counter: str, request: Request):
    await request.add_data(message.from_user.id, message.from_user.first_name)
    # await  bot.send_message(message.from_user.id, f'Welcome {message.from_user.first_name}. Nice to see you!')

    if counter == 1:
        start_message = f'Добро пожаловать, {message.from_user.first_name}, в наш цветочный уголок!'
    else:
        start_message = f'Снова привет, {message.from_user.first_name}!'

    photo = FSInputFile(fr'{settings.bots.content_path}\start-photo.jpg')
    await bot.send_photo(message.chat.id, photo, caption=start_message, reply_markup=start_inline_keyboard())


async def get_location(message: Message, bot: Bot, request: Request):
    await message.answer(f'Я ни в коем случае не сохраняю твою геолокацию \r\n\a'
                         f'<code>{message.location.latitude}\r\n{message.location.longitude}</code> 👀')
    await request.add_location(message.from_user.id, message.location.latitude, message.location.longitude)


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
    try:
        await message.send_copy(chat_id=settings.bots.admin_id)
    except TypeError:
        await bot.send_message(chat_id=settings.bots.admin_id, text='Чтото не то -_-')


async def contacts_info_command(message: Message, bot: Bot):
    await message.answer_location(latitude=52.22885316035805, longitude=21.003265512062914, reply_markup=contacts_inline_keyboard())