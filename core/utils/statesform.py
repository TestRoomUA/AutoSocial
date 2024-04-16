from aiogram.fsm.state import StatesGroup, State


class ChatState(StatesGroup):
    DEFAULT = State()
    BUYING = State()
    SEARCH = State()
    SCROLL = State()


class AdminPanelState(StatesGroup):
    ADMIN = State()


class AdminState(StatesGroup):
    ADD_PRODUCT = State()
    ADDED_PRODUCT_PHOTO = State()
    ADDED_PRODUCT_NAME = State()
    ADDED_PRODUCT_PRICE = State()
    ADDED_PRODUCT_CHECK = State()

    WATCH_LIST = State()
    REMOVE_PRODUCT = State()
