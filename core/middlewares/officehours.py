from datetime import datetime
from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Dict, Any
from aiogram.types import Message, TelegramObject


def office_hours() -> bool:
    return datetime.now().weekday() in (0, 1, 2, 3, 4) and datetime.now().hour in ([i for i in (range(8, 19))])


def always_online() -> bool:
    return datetime.now().weekday() in (0, 1, 2, 3, 4, 5, 6) and datetime.now().hour in ([i for i in (range(0, 24))])


# class OfficeHoursMiddleware(BaseMiddleware):
#     async def __call__(
#             self,
#             handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],  # TelegramObject Or Message
#             event: Message,
#             data: Dict[str, Any],
#     ) -> Any:
#         if office_hours():
#             return await handler(event, data)

class OfficeHoursMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],  # TelegramObject Or Message
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        if always_online():  # office_hours():
            return await handler(event, data)
        await event.answer('Now Bot is sleeping.😴')
