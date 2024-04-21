from typing import List
from aiogram.types import CallbackQuery


class Post:
    def __init__(self, db_id, page, photos, title, price, count):
        self.db_id = db_id
        self.page = page
        self.photos = photos
        self.title = title
        self.price = price
        self.count = count
    db_id: int
    page: int
    photos: List[str]
    title: str
    price: int
    count: int
