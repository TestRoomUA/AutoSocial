import psycopg_pool  # asyncpg


class Request:
    def __init__(self, connector: psycopg_pool.AsyncConnectionPool.connection):  # asyncpg.pool.Pool
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
