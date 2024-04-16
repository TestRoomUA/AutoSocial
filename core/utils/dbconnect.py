import asyncpg  # asyncpg # psycopg_pool
from typing import List
from core.utils.debugger import get_json


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):  # asyncpg.pool.Pool # psycopg_pool.AsyncConnectionPool.connection
        self.connector = connector

    async def add_data(self, user_id: int, user_name):
        query = f"INSERT INTO datausers (user_id, user_name) VALUES ({user_id}, '{user_name}') " \
                f"ON CONFLICT (user_id) DO UPDATE SET user_name='{user_name}'"
        await self.connector.execute(query)

    async def add_age(self, user_id: int, user_age: int):
        query = f"INSERT INTO datausers (user_id, user_age) VALUES ({user_id}, {user_age}) " \
                f"ON CONFLICT (user_id) DO UPDATE SET user_age={user_age}"
        await self.connector.execute(query)

    async def add_location(self, user_id: int, user_location_latitude: float, user_location_longitude: float):
        query = f"INSERT INTO datausers (user_id, user_location_latitude, user_location_longitude) " \
                f"VALUES ({user_id}, {user_location_latitude}, {user_location_longitude}) " \
                f"ON CONFLICT (user_id) " \
                f"DO UPDATE SET user_location_latitude={user_location_latitude}, " \
                f"user_location_longitude={user_location_longitude}"
        await self.connector.execute(query)

    async def add_phone(self, user_id: int, phone):
        query = f"INSERT INTO datausers (user_id, user_phone) VALUES ({user_id}, {phone}) " \
                f"ON CONFLICT (user_id) DO UPDATE SET user_phone={phone}"
        await self.connector.execute(query)

    async def add_order(self, product_id: int, order_price: int, user_id: int, user_name: str, user_address: List[str], user_phone: str):
        address = ', '.join([f"{i if i != '' else None}" for i in user_address])
        query = f"INSERT INTO orders (product_id, order_price, user_id, user_name, user_address, user_phone) VALUES ({product_id}, {order_price}, {user_id}, '{user_name}', '{{ {address} }}'::text[], '{user_phone}') "
        await self.connector.execute(query)

    async def add_product(self, product_name: str, product_price: int, stock: int, photos: List[str]):
        photos_str = ', '.join([f"{photo}" for photo in photos])
        query = f"INSERT INTO products (name, price, count, photos) VALUES ('{product_name}', {product_price}, {stock}, '{{ {photos_str} }}'::text[]) "
        await self.connector.execute(query)

    async def take_product(self, product_id: int):
        try:
            query = f"SELECT * FROM products ORDER BY id ASC OFFSET $1 LIMIT 1"
            result = await self.connector.fetchrow(query, product_id)
            return result
        except asyncpg.PostgresError as e:
            print(e)

    async def take_product_count(self):
        try:
            query = f"SELECT count(*) FROM products"
            result = await self.connector.fetchrow(query)
            return result
        except asyncpg.PostgresError as e:
            print(e)
