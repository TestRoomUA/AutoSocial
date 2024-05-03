from aiogram.fsm.state import StatesGroup, State


class ChatState(StatesGroup):
    MARKET = State()

    BUYING = State()


class AdminPanelState(StatesGroup):
    ADMIN = State()


class AdminState(StatesGroup):
    ADD_PRODUCT = State()
    ADDED_PRODUCT_PHOTO = State()
    ADDED_PRODUCT_NAME = State()
    ADDED_PRODUCT_PRICE = State()
    ADDED_PRODUCT_DESC = State()
    ADDED_PRODUCT_TAGS = State()
    ADDED_PRODUCT_CHECK = State()

    CREATE_POST = State()
    CREATE_POST_BUTTON = State()
    SEND_POST = State()

    WATCH_LIST = State()
    REMOVE_PRODUCT = State()
