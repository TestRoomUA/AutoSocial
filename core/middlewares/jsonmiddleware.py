from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Dict, Any, Callable, Awaitable
from core.utils.debugger import get_json


class JsonMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],  # TelegramObject Or Message
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        await get_json(event)
        return await handler(event, data)
