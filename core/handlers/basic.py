from aiogram import Bot
from aiogram.types import Message
import json
from core.keyboards.reply import loc_tel_keyboard
from core.keyboards.inline import select_car, get_inline_keyboard, start_inline_keyboard
from core.utils.dbconnect import Request


async def get_inline(message: Message, bot: Bot):
    await message.answer(f'Hello, {message.from_user.first_name}. Here inline buttons', reply_markup=get_inline_keyboard())
    await get_json(message)


async def get_start(message: Message, bot: Bot, counter: str, request: Request):
    await request.add_data(message.from_user.id, message.from_user.first_name)
    # await  bot.send_message(message.from_user.id, f'Welcome {message.from_user.first_name}. Nice to see you!')
    if counter == 1:
        await message.answer(f'Привет, {message.from_user.first_name}. Здесь ты узнаешь на что я убил неделю изучения Пайтона🐍😜', reply_markup=start_inline_keyboard())
    else:
        await message.reply(f'Драсьте, {message.from_user.first_name}. Уже виделись 😐', reply_markup=start_inline_keyboard())


async def get_location(message: Message, bot: Bot, request: Request):
    await message.answer(f'Я ни в коем случае не сохраняю твою геолокацию \r\n\a'
                         f'<code>{message.location.latitude}\r\n{message.location.longitude}</code> 👀')
    await request.add_location(message.from_user.id, message.location.latitude, message.location.longitude)


async def get_photo(message: Message, bot: Bot):
    await message.answer(f'Thanks for image <tg-spoiler>...Downloading image...</tg-spoiler>')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, f'photo_{message.photo[-1].file_unique_id}.jpg')
    await get_json(message)


async def get_sticker(message: Message, bot: Bot):
    await message.answer(f'Thanks for sticker <tg-spoiler>...Downloading...</tg-spoiler>')

    file = await bot.get_file(message.sticker.file_id)
    if message.sticker.is_video or message.sticker.is_animated:
        await bot.download_file(file.file_path, f'sticker-video-{message.sticker.file_unique_id}.mp4')
    else:
        await bot.download_file(file.file_path, f'sticker-image-{message.sticker.file_unique_id}.jpg')
    await get_json(message)
    await message.reply(f'Done!')


async def get_voice(message: Message, bot: Bot):
    await message.answer(f'Wow nice voice! <tg-spoiler>...Downloading...</tg-spoiler>')
    file = await bot.get_file(message.voice.file_id)
    await bot.download_file(file.file_path, f'voice-{message.voice.file_unique_id}.wav')
    await get_json(message)


async def get_hello(message: Message, bot: Bot):
    await message.answer(f'Helloo you too, {message.from_user.first_name}!!!')
    await get_json(message)


async def get_repeat(message: Message, bot: Bot):
    user_text = message.text
    await message.answer(f'Сам ты: {user_text}')
    await get_json(message)


async def get_json(message: Message):
    json_str = json.dumps(message.dict(), default=str, indent=4)
    print(json_str)
    return json_str
