from aiogram.types import Message, FSInputFile, InputMediaPhoto, InputMediaVideo
from aiogram import Bot
from aiogram.utils.chat_action import ChatActionSender


async def get_audio(message: Message, bot: Bot):
    audio = FSInputFile(path=r'E:\PET-PROJECTS\AutoSocial\voice-AgADv0EAAhzVoEs.wav', filename='AudioFile.wav')
    await bot.send_audio(message.chat.id, audio=audio)


async def get_document(message: Message, bot: Bot):
    document = FSInputFile(path=r'E:\PET-PROJECTS\AutoSocial\FILE.txt')
    await bot.send_document(message.chat.id, document=document, caption='Its DOCUMENT')


async def get_media_group(message: Message, bot: Bot):
    photo1_mg = InputMediaPhoto(type='photo', media=FSInputFile(r'E:\PET-PROJECTS\AutoSocial\sticker-image-AgADIgEAAhzfMRU.png'),
                                caption='Its photo')
    photo2_mg = InputMediaPhoto(type='photo', media=FSInputFile(r'E:\PET-PROJECTS\AutoSocial\sticker-image-AgADuDkAAg2rsUs.png'),
                                caption='Its photo too')
    video1_mg = InputMediaVideo(type='video', media=FSInputFile(r'E:\PET-PROJECTS\AutoSocial\sticker-video-AgADtRkAAlVoaEo.mp4'),
                                caption='Now its video')
    video2_mg = InputMediaVideo(type='video', media=FSInputFile(r'E:\PET-PROJECTS\AutoSocial\sticker-video-AgADDDgAAhp4IEo.mp4'))
    media = [photo2_mg, photo1_mg, video2_mg, video1_mg]
    await bot.send_media_group(message.chat.id, media)


async def get_photo(message: Message, bot: Bot):
    photo = FSInputFile(r'E:\PET-PROJECTS\AutoSocial\sticker-image-AgADwSEAAvNoGUk.png')
    await bot.send_photo(message.chat.id, photo, caption='Photo')


async def get_sticker(message: Message, bot: Bot):
    sticker = FSInputFile(r'E:\PET-PROJECTS\AutoSocial\sticker-image-AgAD2QADTqDDMA.png')
    await bot.send_sticker(message.chat.id, sticker)


async def get_video(message: Message, bot: Bot):
    async with ChatActionSender.upload_video(message.chat.id, bot):
        video = FSInputFile(r'E:\PET-PROJECTS\AutoSocial\sticker-video-AgADtRkAAlVoaEo.mp4')
        await bot.send_video(message.chat.id, video)


async def get_video_note(message: Message, bot: Bot):
    async with ChatActionSender.upload_video_note(message.chat.id, bot):
        video = FSInputFile(r'E:\PET-PROJECTS\AutoSocial\sticker-video-AgADtRkAAlVoaEo.mp4')
        await bot.send_video_note(message.chat.id, video)


async def get_voice(message: Message, bot: Bot):
    async with ChatActionSender.record_voice(message.chat.id, bot):
        voice = FSInputFile(r'E:\PET-PROJECTS\AutoSocial\voice-AgADv0EAAhzVoEs.wav')
        await bot.send_voice(message.chat.id, voice)
