from aiogram.filters.callback_data import CallbackData


class ProductInfo(CallbackData, prefix='product'):
    type: str
    name: str
    index: int
    description: str
    color: str
    price: int
    inStock: int


class ProductID(CallbackData, prefix='productID'):
    id: int
