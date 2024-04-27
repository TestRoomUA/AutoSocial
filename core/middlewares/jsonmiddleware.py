from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Dict, Any, Callable, Awaitable
from core.utils.debugger import get_json, get_json_call


class JsonMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],  # TelegramObject Or Message
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        await get_json(event)
        return await handler(event, data)


class JsonCallMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],  # TelegramObject Or Message
            event: CallbackQuery,
            data: Dict[str, Any],
    ) -> Any:
        await get_json_call(event)
        return await handler(event, data)