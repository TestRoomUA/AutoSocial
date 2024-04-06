from typing import Callable, Awaitable, Dict, Any
from psycopg_pool import AsyncConnectionPool
# import asyncpg
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from core.utils.dbconnect import Request


class DbSession(BaseMiddleware):
    def __init__(self, connector: AsyncConnectionPool):  # asyncpg.pool.Pool
        super().__init__()
        self.connector = connector

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any],
    ) -> Any:
        async with self.connector.connection() as connect:  # .acquire()
            data['request'] = Request(connect)
            return await handler(event, data)
