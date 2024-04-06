from aiogram.types import Message
from aiogram import Bot
from core.utils.dbconnect import Request


async def get_true_contact(message: Message, bot: Bot, phone: str, request: Request):
    await message.answer(f'Красивый номер телефона, {message.chat.first_name}! Я даже и не думал его себе сохранять, не переживай 👀')
    await request.add_phone(message.from_user.id, phone)


async def get_fake_contact(message: Message, bot: Bot):
    await message.answer(f'Не ври мне! Это не твой номер 😑')
