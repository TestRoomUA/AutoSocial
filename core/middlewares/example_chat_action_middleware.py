from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message, TelegramObject
from aiogram.utils.chat_action import ChatActionSender


class ExampleChatActionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        chat_action = get_flag(data, 'chat_action')
        if not chat_action:
            return await handler(event, data)
        bot = data["bot"]

        async with ChatActionSender(bot=bot, action=chat_action, chat_id=event.chat.id):
            return await handler(event, data)
