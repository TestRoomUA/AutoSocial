from datetime import datetime
from typing import List

import asyncpg  # asyncpg # psycopg_pool


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):  # asyncpg.pool.Pool # psycopg_pool.AsyncConnectionPool.connection
        self.connector = connector

    async def add_userdata(self, user_id: int, user_name: str, date: datetime):
        query = f"INSERT INTO datausers (user_id, user_name, start_date) VALUES ($1, $2, $3) " \
                f"ON CONFLICT (user_id) DO UPDATE SET user_name=$2, last_online=$3 "
        await self.connector.execute(query, user_id, user_name, date)
        # querytest = f"UPDATE datausers SET start_date=$1"
        # await self.connector.execute(querytest, date)

    async def update_user_online(self, user_id: int, date: datetime):
        query = f"UPDATE datausers SET last_online=$2 WHERE user_id=$1"
        await self.connector.execute(query, user_id, date)

    async def add_content(self, file_id: str, path: str, filename: str):
        try:
            query_create_table = f"CREATE TABLE IF NOT EXISTS contentdata ( " \
                    f"file_id text NOT NULL, " \
                    f"path text NOT NULL, " \
                    f"filename text NOT NULL, " \
                    f"id integer NOT NULL GENERATED ALWAYS AS IDENTITY, " \
                    f"PRIMARY KEY (id) ); "

            query = f"INSERT INTO contentdata (file_id, path, filename) VALUES ($1, $2, $3) " \
                    f"ON CONFLICT (id) DO NOTHING " \
                    f"RETURNING id; "
            await self.connector.execute(query_create_table)
            result = await self.connector.fetchrow(query, file_id, path, filename)
            return result
        except asyncpg.PostgresError as e:
            print(e)

    # async def take_content(self, content_id: int):
    #     try:
    #         query = f"SELECT * FROM contentdata WHERE id = $1"
    #         result = await self.connector.fetchrow(query, content_id)
    #         return result
    #     except asyncpg.PostgresError as e:
    #         print(e)

    async def take_file_ids(self, content_ids: List[int]):
        try:
            query = f"SELECT file_id FROM contentdata WHERE id IN ({','.join(map(str, content_ids))})"
            result = await self.connector.fetch(query)
            return result
        except asyncpg.PostgresError as e:
            print(f'{e} \r\n-------\r\n {content_ids}')

    async def add_order(self, product_id: int, order_price: int, user_id: int, user_name: str, user_address: List[str], user_phone: str):
        address = ', '.join([f"{i if i != '' else None}" for i in user_address])
        query = f"INSERT INTO orders (product_id, order_price, user_id, user_name, user_address, user_phone) VALUES ({product_id}, {order_price}, {user_id}, '{user_name}', '{{ {address} }}'::text[], '{user_phone}') "
        await self.connector.execute(query)

    async def add_product(self, product_name: str, product_price: int, count: int, content_ids: List[int], desc: str, tags: List[str]):
        try:
            # photos_str = ', '.join([f"{photo}" for photo in photos])
            query = \
                f"""INSERT INTO products (name, price, count, content_ids{', description' if desc is not None else ''}{', tags' if tags is not None else ''}) 
                VALUES ($1, $2, $3, $4::int[], $5', {{ {', '.join([f"'{tag}'" for tag in tags])} }}'::text[]') 
                RETURNING id;"""
            result = await self.connector.fetchrow(query, product_name, product_price, count, content_ids, desc)
            return result
        except asyncpg.PostgresError as e:
            print(e)

    async def take_product(self, row_num: int):
        try:
            query = f"SELECT * FROM products " \
                    f"ORDER BY id ASC OFFSET $1 LIMIT 1"
            result = await self.connector.fetchrow(query, row_num)
            return result
        except asyncpg.PostgresError as e:
            print(e)

    async def take_product_by_id(self, db_id: int):
        try:
            query = f"SELECT * FROM ( SELECT *, ROW_NUMBER() OVER ( ORDER BY id ) AS rnum " \
                    f"FROM products ) x WHERE id = $1"
            result = await self.connector.fetchrow(query, db_id)
            return result
        except asyncpg.PostgresError as e:
            print(e)

    async def take_product_count(self):
        try:
            query = f"SELECT count(*) as r_max FROM products"
            result = await self.connector.fetchrow(query)
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
