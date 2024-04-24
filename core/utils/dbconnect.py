from datetime import datetime
from typing import List

import asyncpg  # asyncpg # psycopg_pool


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):  # asyncpg.pool.Pool # psycopg_pool.AsyncConnectionPool.connection
        self.connector = connector

    async def add_userdata(self, user_id: int, user_name: str, date: datetime):
        formatted_date = date.astimezone().strftime('%Y-%m-%d %H:%M:%S%z')
        timestamp = date.timestamp()
        query = f"INSERT INTO datausers (user_id, user_name, start_date) VALUES ($1, $2, $3) " \
                f"ON CONFLICT (user_id) DO UPDATE SET user_name=$2, last_online=$3 "
        await self.connector.execute(query, user_id, user_name, date)
        # querytest = f"UPDATE datausers SET start_date=$1"
        # await self.connector.execute(querytest, date)

    async def update_user_online(self, user_id: int, date: datetime):
        query = f"UPDATE datausers SET last_online=$2 WHERE user_id=$1"
        await self.connector.execute(query, user_id, date)

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
        try:
            photos_str = ', '.join([f"{photo}" for photo in photos])
            query = f"INSERT INTO products (name, price, count, photos) " \
                    f"VALUES ('{product_name}', {product_price}, {stock}, '{{ {photos_str} }}'::text[]) " \
                    f"RETURNING id;"
            result = await self.connector.fetchrow(query)
            return result
        except asyncpg.PostgresError as e:
            print(e)

    async def take_product(self, product_id: int):
        try:
            query = f"SELECT *, ROW_NUMBER() OVER () AS rnum " \
                    f"FROM products ORDER BY id ASC OFFSET $1 LIMIT 1;"
            result = await self.connector.fetchrow(query, product_id)
            return result
        except asyncpg.PostgresError as e:
            print(e)

    async def take_product_by_id(self, db_id: int):
        query = ""
        try:
            query = f"SELECT * FROM ( SELECT *, ROW_NUMBER() OVER ( ORDER BY id ) AS rnum " \
                    f"FROM products ) x WHERE id = {db_id}"
            result = await self.connector.fetchrow(query)
            return result
        except asyncpg.PostgresError as e:
            print(query)
            print(e)

    async def take_product_count(self):
        try:
            query = f"SELECT count(*) FROM products"
            result = await self.connector.fetchrow(query)
            print(result)
            return result
        except asyncpg.PostgresError as e:
            print(e)

    async def take_new_count(self):
        try:
            query = f"SELECT count(*) as new, new_count as old FROM products, datatest ORDER BY datatest.id DESC LIMIT 1" \
                    f"INSERT INTO datatest (new_count) VALUES (new)"
            req = await self.connector.fetchrow(query)
            result = req['new'] - req['old']
            return result
        except asyncpg.PostgresError as e:
            print(e)