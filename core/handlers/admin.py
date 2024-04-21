from typing import List

from aiogram import Bot
from aiogram.types import Message, FSInputFile, InputMediaPhoto, CallbackQuery
from core.keyboards.inline import admin_keyboard, product_test_keyboard
from core.keyboards.reply import admin_add_photo_reply_keyboard
from core.utils.dbconnect import Request
from aiogram.fsm.context import FSMContext
from core.utils.statesform import AdminState, AdminPanelState
from core.utils.objects import Post
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.handlers.apsched import post_channel
from datetime import datetime, timedelta
from core.settings import settings


async def admin_mode(message: Message, bot: Bot, state: FSMContext):
    if not message.from_user.id == settings.bots.admin_id:
        return

    await state.set_state(AdminPanelState.ADMIN)
    msg = f'{message.from_user.first_name}, вы зашли в Админ панель!'

    photo = FSInputFile(fr'{settings.media.content}\0.png')
    await bot.send_photo(message.chat.id, photo, caption=msg, reply_markup=admin_keyboard())


async def admin_callback(call: CallbackQuery, bot: Bot, state: FSMContext, request: Request):
    data = call.data.split('_')
    match data[1]:
        case 'logout':
            await state.clear()
            await call.message.answer('Вы вышли с панели админа')
        case 'product':
            match data[2]:
                case 'add':
                    await state.set_state(AdminState.ADD_PRODUCT)
                    await call.message.answer('Отправьте фотографию (фотографии) нового продукта')
                case 'list':
                    await state.set_state(AdminState.WATCH_LIST)
                    post_data = await request.take_product(3)
                    photo = FSInputFile(fr"{settings.media.content}\{post_data['photos'][0]}")
                    name = post_data['name']
                    price = post_data['price']
                    count = post_data['count']
                    await call.bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=f"{name}\r\n Цена: {price} zł\r\n{count} в букете")
                case 'remove':
                    await state.set_state(AdminState.REMOVE_PRODUCT)
                    await call.message.answer('Введите номер продукта, который хотите убрать')

    await call.answer()


async def add_product_photo(message: Message, bot: Bot, state: FSMContext):
    context_data = await state.get_data()
    photos: List[str] = context_data.get(f'photos') if context_data.get(f'photos') is not None else []
    photos_len = len(photos) + 1
    if photos_len > 3:
        await message.answer(text='Лимит фото превышен. \r\nЕлси что-то не так, обратитесь к разработчику')
        await message.send_copy(chat_id=settings.bots.admin_id)
        await bot.send_message(chat_id=settings.bots.admin_id, text='Хозяин хочет больше фото!!!')
        return

    file = await bot.get_file(message.photo[-1].file_id)
    filename = fr'p_{message.photo[-1].file_unique_id}.jpg'
    await bot.download_file(file.file_path, fr'Content\{filename}')
    photos.append(filename)
    await state.update_data(photos=photos)

    if photos_len == 3:
        await message.answer(text='Отлично, теперь отправьте название продукта')
        await state.set_state(AdminState.ADDED_PRODUCT_PHOTO)
        return

    if photos_len < 3:
        await message.answer(text=f'Получено {photos_len} из 3 фото. Вы можете добавить ещё, либо оставить {photos_len} фото и перейти к названию', reply_markup=admin_add_photo_reply_keyboard())
        return


async def button_next_added_product_photo(message: Message, bot: Bot, state: FSMContext):
    await message.answer(text='Отлично, теперь отправьте название продукта')
    await state.set_state(AdminState.ADDED_PRODUCT_PHOTO)


async def add_product_name(message: Message, bot: Bot, state: FSMContext):
    name = message.text
    await message.answer(f'Назовите цену для {name}')
    await state.update_data(name=name)
    await state.set_state(AdminState.ADDED_PRODUCT_NAME)


async def add_product_price(message: Message, bot: Bot, state: FSMContext):
    price = int(message.text)
    await state.update_data(price=price)
    await message.answer(f'Сколько цветов в букете?')
    await state.set_state(AdminState.ADDED_PRODUCT_PRICE)


async def add_product_quantity(message: Message, bot: Bot, state: FSMContext):
    count = int(message.text)
    await state.update_data(count=count)
    await message.answer(f'Данные готовы, так выглядит ваш продукт. Елси всё супер, скажите Далее')
    context_data = await state.get_data()
    name = context_data.get('name')
    photos = context_data.get('photos')
    price = context_data.get('price')
    media = [InputMediaPhoto(type='photo', media=FSInputFile(fr"{settings.media.content}\{photo}")) for photo in photos]
    media[0].caption = f'{name}\r\n{price}zł \r\nВ наличии: {count}'
    media[0].reply_markup = product_test_keyboard()
    await bot.send_media_group(chat_id=message.chat.id, media=media)
    await state.set_state(AdminState.ADDED_PRODUCT_CHECK)


async def add_product_check_successful(message: Message, bot: Bot, state: FSMContext, request: Request, apscheduler: AsyncIOScheduler):
    await message.answer('perfect')
    context_data = await state.get_data()
    name = context_data.get('name')
    photos = context_data.get('photos')
    price = context_data.get('price')
    count = context_data.get('count')
    db_answer = await request.add_product(name, price, count, photos)
    db_count = await request.take_product_count()
    apscheduler.add_job(post_channel,
                        trigger='date',
                        run_date=datetime.now() + timedelta(seconds=10),
                        kwargs={'bot': bot, 'post': Post(db_id=db_answer['id'],
                                                         page=db_count,
                                                         photos=photos,
                                                         title=name,
                                                         price=price,
                                                         count=count)})
    await state.clear()


async def add_product_check_fail(message: Message, bot: Bot, state: FSMContext):
    await message.answer('Штож, повторим. Пришлите фото продукта')
    await state.clear()
    await state.set_state(AdminState.ADD_PRODUCT)