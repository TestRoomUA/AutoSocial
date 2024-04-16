import json
from aiogram.types import Message, CallbackQuery


async def get_json(message: Message):
    json_str = json.dumps(message.dict(), default=str, indent=4)
    print('\r\n' + json_str + '\r\n')
    return json_str


async def test_button(call: CallbackQuery):
    await call.answer(text="Тестовая кнопка!", cache_time=30)
