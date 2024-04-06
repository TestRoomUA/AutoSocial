from aiogram.filters.callback_data import CallbackData


class CarInfo(CallbackData, prefix='car'):
    brand: str
    model: str
    color: str
    year: int


