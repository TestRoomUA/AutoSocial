from typing import List


class TextInfo:
    def __init__(self, title=None, price=None, desc=None, tags=None, count=None):
        if title is not None: self.title = title
        if price is not None: self.price = price
        if desc is not None: self.desc = desc
        if tags is not None: self.tags = tags
        if count is not None: self.count = count

    title: str
    price: int
    desc: str
    tags: List[str]
    count: int


class MediaInfo:
    def __init__(self, file_ids=None):
        if file_ids is not None: self.file_ids = file_ids
    file_ids: List[str]


class DBInfo:
    def __init__(self, db_id=None, page=None):
        if db_id is not None: self.db_id = db_id
        if page is not None: self.page = page

    db_id: int
    page: int


class Post:
    def __init__(self, db_id, page, file_ids, title, price, count, desc=None, tags=None):
        self.db = DBInfo(db_id, page)
        self.db_id = db_id
        self.page = page
        self.media = MediaInfo(file_ids)
        self.file_ids = file_ids
        self.text = TextInfo(title=title, price=price, desc=desc, tags=tags, count=count)
        self.title = title
        self.price = price
        self.count = count
        self.desc = desc
        self.tags = tags
                                                                                        # ХВАТИТ
    db_id: int
    page: int
    file_ids: List[str]
    title: str
    price: int
    desc: str
    tags: List[str]
    count: int
    text: TextInfo
    media: MediaInfo
    db: DBInfo

