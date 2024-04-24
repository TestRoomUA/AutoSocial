from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Dict, Any, Callable, Awaitable
from core.settings import settings


class GuestCounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.guest_message_counter = 0
        self.last_user_id = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        if event.chat.id == settings.bots.admin_id or event.bot is None:
            self.last_user_id = settings.bots.admin_id
        else:
            if event.chat.id != self.last_user_id:
                self.last_user_id = event.chat.id
                self.guest_message_counter = 0
            if self.guest_message_counter == 0:
                await event.bot.send_message(chat_id=settings.bots.admin_id, text=f'У нас гости 👀\r\n{event.from_user.first_name}\r\n{event.from_user.id}')
            self.guest_message_counter += 1
            await event.bot.copy_message(chat_id=settings.bots.admin_id, from_chat_id=event.chat.id, message_id=event.message_id)

        data['guest_message_counter'] = self.guest_message_counter
        data['last_user_id'] = self.last_user_id
        return await handler(event, data)