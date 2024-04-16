from aiogram import Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, InlineKeyboardButton, InlineKeyboardMarkup,\
    ShippingOption, ShippingQuery, FSInputFile
from core.utils.callbackdata import ProductInfo
from aiogram.types import CallbackQuery
from core.utils.dbconnect import Request
from core.utils.debugger import get_json
from core.settings import settings
from core.utils.callbackdata import ProductInfo

keyboards = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='to Pay order',
            pay=True
        )
    ],
    [
        InlineKeyboardButton(
            text='link',
            url='https://google.com'
        )
    ]
])


PL_SHIPPING = ShippingOption(
    id='pl',
    title='Delivery to Poland',
    prices=[
        LabeledPrice(
            label='Delivery InPost',
            amount=1000
        ),
        LabeledPrice(
            label='Доставка в руки',
            amount=2000
        )
    ]
)

UA_SHIPPING = ShippingOption(
    id='ua',
    title='Delivery to Ukraine',
    prices=[
        LabeledPrice(
            label='Delivery UPS',
            amount=1000
        )
    ]
)

CITIES_SHIPPING = ShippingOption(
    id='capitals',
    title='Fast city delivery',
    prices=[
        LabeledPrice(
            label='Доставка в руки',
            amount=2000
        )
    ]
)


# 4111 1111 1111 1111
async def shipping_check(shipping_query: ShippingQuery, bot: Bot):
    shipping_options = []
    countries = ['PL', 'UA']
    if shipping_query.shipping_address.country_code not in countries:
        return await bot.answer_shipping_query(shipping_query.id, ok=False,
                                               error_message='We dont make deliveries to this country:(')
    if shipping_query.shipping_address.country_code.lower() == 'pl':
        shipping_options.append(PL_SHIPPING)

    if shipping_query.shipping_address.country_code.lower() == 'ua':
        shipping_options.append(UA_SHIPPING)

    cities = ['Warsaw', 'Warszawa']
    if shipping_query.shipping_address.city in cities:
        shipping_options.append(CITIES_SHIPPING)

    await bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options)


async def order(call: CallbackQuery, bot: Bot, request: Request):
    call_data = call.data.split('_')
    index = int(call_data[1])
    post_data = await request.take_product(index)
    desc = post_data['description']
    if desc is None:
        desc = ""
    await bot.send_invoice(
        chat_id=call.message.chat.id,
        title=f"{post_data['name']}\r\n",
        description=f"{desc} \r\n{post_data['count']} в букете \r\n",
        payload=str(index),
        provider_token='410694247:TEST:c3421322-ca26-442d-8f7d-553c98ba2076',
        currency='PLN',
        prices=[
            LabeledPrice(
                label='Купить один букет',
                amount=post_data['price'] * 100
            ),
            LabeledPrice(
                label='Discount',
                amount=-500
            )
        ],
        max_tip_amount=20000,
        suggested_tip_amounts=[500, 1500, 5000, 15000],
        start_parameter='',
        provider_data=None,
        photo_url=fr"{settings.bots.content_path}\{post_data['photos'][0]}",
        photo_size=100,
        photo_width=800,
        photo_height=800,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=True,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=keyboards,
        request_timeout=15
    )


async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def successful_payment(message: Message, request: Request):
    productID = int(message.successful_payment.invoice_payload)
    await get_json(message)

    post_data = await request.take_product(productID)
    productID = post_data['id']

    total_amount = message.successful_payment.total_amount // 100
    currency = message.successful_payment.currency

    msg = f'Спасибо что выбрали нас! Оплата прошла успешно:  {total_amount}.00 {currency}. \r\n' \
          f'Скоро наш менеджер свяжеться с вами для уточнения деталей. \r\n'
    photo = FSInputFile(fr'{settings.bots.content_path}\success-payment.jpg')
    await message.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=msg)

    user_id = message.from_user.id
    user_name = message.successful_payment.order_info.name

    shipping_address = message.successful_payment.order_info.shipping_address
    user_address = [shipping_address.country_code, shipping_address.state, shipping_address.city,
                    shipping_address.street_line1, shipping_address.street_line2, shipping_address.post_code]
    print(user_address)
    user_phone = message.successful_payment.order_info.phone_number
    await request.add_order(productID, total_amount, user_id, user_name, user_address, user_phone)
