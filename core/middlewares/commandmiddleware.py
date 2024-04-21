from aiogram import BaseMiddleware
from aiogram.filters import CommandObject
from aiogram.types import Message
from typing import Dict, Any, Callable, Awaitable


class CommandMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        data['command'] = CommandObject()
        return await handler(event, data)
