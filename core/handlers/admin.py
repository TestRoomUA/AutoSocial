import asyncio
from typing import List

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto, InputMedia, ContentType as CT
from core.keyboards.inline import admin_keyboard, added_product
from core.keyboards.reply import next_reply_keyboard
from core.utils.dbconnect import Request
from aiogram.fsm.context import FSMContext
from core.utils.states import AdminState, AdminPanelState
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.utils.deep_linking import create_start_link
from core.handlers.media import post_text
from core.settings import settings
from core.handlers.channel import send_post_to_channel


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
                    await bot.send_message(chat_id=call.message.chat.id, text='Отправьте фотографию (фотографии) нового продукта')
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
        case 'post':
            match data[2]:
                case 'channel':
                    await state.set_state(AdminState.CREATE_POST)
                    await bot.send_message(chat_id=call.message.chat.id,
                                           text='Введите текст поста, если хотите добавьте картинку')
    chat = call.message.chat.id
    message_id = call.message.message_id
    await call.answer()
    await bot.delete_message(chat_id=chat, message_id=message_id)


async def add_product_photo_group(message: Message, bot: Bot, state: FSMContext, album: List[Message] = None):
    media_max = settings.media.post_media_max
    context_data = await state.get_data()
    file_ids: List[str] = context_data.get(f'file_ids') if context_data.get(f'file_ids') is not None else []
    photo_len = len(file_ids)
    is_max = False

    for i, msg in enumerate(album) if album is not None else enumerate([message]):
        media_len = photo_len + i + 1
        if media_len > media_max:
            await message.answer(
                text=f'Лимит медиа превышен (максимум: {media_max}). \r\nЕлси что-то не так, обратитесь к разработчику')
            await message.send_copy(chat_id=settings.bots.admin_id)
            await bot.send_message(chat_id=settings.bots.admin_id, text='Хозяин хочет больше фото!!!')
            break

        if msg.photo:
            file_id = msg.photo[-1].file_id
        else:
            obj_dict = msg.model_dump()
            file_id = obj_dict[msg.content_type]['file_id']

        file_ids.append(file_id)
        message_media_count = f'Получено {media_len} из {media_max} фото. '

        await bot.send_message(chat_id=message.chat.id, text=message_media_count)
        if media_len == media_max:
            is_max = True
    if is_max:
        await button_next_added_product_photo(message=message, bot=bot, state=state)
    else:
        await bot.send_message(chat_id=message.chat.id, reply_markup=next_reply_keyboard('Отправьте ещё фото, либо нажмите кнопку "Далее"'),
                               text=f'Добавьте ещё, либо нажмите "Далее", чтобы перейти к названию')

    await state.update_data(file_ids=file_ids)


async def button_next_added_product_photo(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Отлично, теперь отправьте название продукта')
    await state.set_state(AdminState.ADDED_PRODUCT_PHOTO)


async def add_product_name(message: Message, bot: Bot, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await state.set_state(AdminState.ADDED_PRODUCT_NAME)
    await bot.send_message(chat_id=message.chat.id, text=f'Назовите цену для {name}')


async def add_product_price(message: Message, bot: Bot, state: FSMContext):
    price = int(message.text)
    await state.update_data(price=price)
    await state.set_state(AdminState.ADDED_PRODUCT_PRICE)
    await bot.send_message(chat_id=message.chat.id, text=f'Добавьте описание продукту')


async def add_product_description(message: Message, bot: Bot, state: FSMContext):
    description: str | None = message.text if message.text.lower() != 'далее' else None
    await state.update_data(description=description)
    await state.set_state(AdminState.ADDED_PRODUCT_DESC)
    await bot.send_message(chat_id=message.chat.id, text=f'Добавьте категории для продукта (пишите категории через запятую (,) )')


async def add_product_tags(message: Message, bot: Bot, state: FSMContext):
    tags: List[str] = [tag.strip() for tag in message.text.strip().split(',')]
    await state.update_data(tags=tags)
    await state.set_state(AdminState.ADDED_PRODUCT_TAGS)
    await bot.send_message(chat_id=message.chat.id, text=f'Если хотите, укажите сколько в наличии цветов')


async def add_product_quantity(message: Message, bot: Bot, state: FSMContext, request: Request):
    count = int(message.text)
    await state.update_data(count=count)
    wait_msg = await bot.send_message(chat_id=message.chat.id, text=f'Подождите. Идёт загрузка.')
    context_data = await state.get_data()
    name = context_data.get('name')
    file_ids = context_data.get('file_ids')
    price = context_data.get('price')
    description = context_data.get('description')
    tags = context_data.get('tags')
    name_for_file = name.replace(" ", "_")
    media = []
    content_ids = []
    for i, file_id in enumerate(file_ids):
        file = await bot.get_file(file_id)
        filename = fr'p_{name_for_file}-{i+1}.jpg'
        filepath = settings.media.content
        await bot.download_file(file.file_path, fr'{filepath}\{filename}')
        content_id = await request.add_content(file_id=file_id, path=filepath, filename=filename)
        content_ids.append(content_id['id'])
        media.append(InputMediaPhoto(type='photo', media=file_id))
        wait_msg = await bot.edit_message_text(chat_id=wait_msg.chat.id, message_id=wait_msg.message_id, text=wait_msg.text+'.')
        await asyncio.sleep(0.01)
    await bot.edit_message_text(chat_id=wait_msg.chat.id, message_id=wait_msg.message_id,
                                text=f'Данные готовы! Так выглядит ваш продукт.')
    text = post_text(name, price, count, description, tags)
    media[0].caption = text
    await bot.send_media_group(chat_id=message.chat.id, media=media)
    await bot.send_message(chat_id=message.chat.id, reply_markup=next_reply_keyboard('Нажмите кнопку "Далее", для отмены введите любое другое слово'), text='Если всё супер, скажите "Далее"')
    await state.update_data(content_ids=content_ids)
    await state.set_state(AdminState.ADDED_PRODUCT_CHECK)


async def add_product_check_successful(message: Message, bot: Bot, state: FSMContext, request: Request, apscheduler: AsyncIOScheduler):
    context_data = await state.get_data()
    name = context_data.get('name')
    content_ids = context_data.get('content_ids')
    price = context_data.get('price')
    count = context_data.get('count')
    description = context_data.get('description')
    tags = context_data.get('tags')
    db_answer = await request.add_product(name, price, count, content_ids, description, tags)
    db_id = db_answer['id']
    await bot.send_message(chat_id=message.chat.id, text='Готово! Выберите действие', reply_markup=added_product(db_id))
    await state.clear()
    await state.set_state(AdminPanelState.ADMIN)


async def add_product_check_fail(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Штож, повторим. Пришлите фото продукта')
    await state.clear()
    await state.set_state(AdminState.ADD_PRODUCT)


async def create_post(message: Message, bot: Bot, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    chat = message.chat.id
    if message.photo:
        file_id = message.photo[-1].file_id
        await state.update_data(photo_file_id=file_id)
        await bot.send_photo(chat_id=chat, photo=file_id, caption=text)
    elif message.video:
        file_id = message.video.file_id
        await state.update_data(video_file_id=file_id)
        await bot.send_video(chat_id=chat, video=file_id, caption=text)
    else:
        await bot.send_message(chat_id=chat, text=text)
    await state.set_state(AdminState.CREATE_POST_BUTTON)
    await bot.send_message(chat_id=chat, text='Теперь давайте добавим кнопку. Введи название кнопки')


async def create_post_button(message: Message, bot: Bot, state: FSMContext):
    text = message.text
    chat = message.chat.id
    state_data = await state.get_data()
    if state_data.get('btn_text') is None:
        await state.update_data(btn_text=text)
        await bot.send_message(chat_id=chat, text='Теперь отправьте ссылку для кнопки, либо нажмите "Далее" и кнопка будет с ссылкой на бота', reply_markup=next_reply_keyboard('Отправьте ссылку, либо нажмите кнопку "Далее"'))
    else:
        if text.lower() == 'далее':
            link = await create_start_link(bot=bot, payload='from_channel', encode=True)
        else:
            link = text
        await send_post_to_channel(settings.channel.id, bot, state_data.get('text'), state_data.get('photo_file_id'), state_data.get('video_file_id'), state_data.get('btn_text'), link)
        await bot.send_message(chat_id=chat, text='Готово!')
        await state.clear()
