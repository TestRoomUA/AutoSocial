from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.utils.dbconnect import Request
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.handlers.apsched import send_message_middleware
from datetime import datetime, timedelta
from aiogram import Bot


# async def get_form(message: Message, state: FSMContext):
#     await message.answer(f'{message.from_user.first_name}, starting form. Write your name, please')
#     await state.set_state(StepsForm.GET_NAME)
#
#
# async def get_name(message: Message, state: FSMContext):
#     await message.answer(f'Your name is: \r\n{message.text}\r\n Now Write your last name')
#     await state.update_data(name=message.text)
#     await state.set_state(StepsForm.GET_LAST_NAME)
#
#
# async def get_last_name(message: Message, state: FSMContext):
#     await message.answer(f'Your last name is:\r\n{message.text}\r\n Now write your age')
#     await state.update_data(last_name=message.text)
#     await state.set_state(StepsForm.GET_AGE)
#
#
# async def get_age(message: Message, bot: Bot, state: FSMContext, request: Request, apscheduler: AsyncIOScheduler):
#     context_data = await state.get_data()
#     # await message.answer(f'All saved data in Machine States: {str(context_data)}')
#     name = context_data.get('name')
#     last_name = context_data.get('last_name')
#     age = int(message.text)
#     if age >= 18:
#         await message.answer(f'ГОДЕНН!!!! Открывай двери:)')
#     else:
#         minus = 18 - age
#         match minus:
#             case 1:
#                 year_word = 'год'
#             case 2, 3, 4:
#                 year_word = 'года'
#             case _:
#                 year_word = 'лет'
#
#         await message.answer(f'вот ваша повестк.. а блин, ладно вернусь через {minus} {year_word}')
#     print(age)
#     data_user = f'Мы записали запомнили📝:\r\n' \
#                 f'{name}\r\n' \
#                 f'{last_name}\r\n' \
#                 f'Лет: {age}'
#     await message.answer(data_user)
#     await state.clear()
#     await request.add_age(message.from_user.id, age)
#     apscheduler.add_job(send_message_middleware, trigger='date', run_date=datetime.now() + timedelta(seconds=10),
#                         kwargs={'bot': bot, 'chat_id': message.from_user.id})
