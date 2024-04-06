from aiogram import Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, InlineKeyboardButton, InlineKeyboardMarkup,\
    ShippingOption, ShippingQuery


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
            amount=500
        ),
        LabeledPrice(
            label='Delivery DPD',
            amount=700
        )
    ]
)

EU_SHIPPING = ShippingOption(
    id='eu',
    title='Delivery to Europe',
    prices=[
        LabeledPrice(
            label='Delivery UPS',
            amount=10000
        )
    ]
)

CITIES_SHIPPING = ShippingOption(
    id='capitals',
    title='Fast city delivery',
    prices=[
        LabeledPrice(
            label='Courier delivery',
            amount=2000
        )
    ]
)


async def shipping_check(shipping_query:ShippingQuery, bot: Bot):
    shipping_options = []
    countries = ['PL', 'EU']
    if shipping_query.shipping_address.country_code not in countries:
        return await bot.answer_shipping_query(shipping_query.id, ok=False,
                                               error_message='We dont make deliveries to this country:(')
    if shipping_query.shipping_address.country_code == 'PL':
        shipping_options.append(PL_SHIPPING)

    if shipping_query.shipping_address.country_code == 'EU':
        shipping_options.append(EU_SHIPPING)

    cities = ['Warsaw']
    if shipping_query.shipping_address.city in cities:
        shipping_options.append(CITIES_SHIPPING)

    await bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options)


async def order(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Telegram Bot Test Payment',
        description='Studing to make payments',
        payload='Payment through a bot',
        provider_token='410694247:TEST:c3421322-ca26-442d-8f7d-553c98ba2076',
        currency='pln',
        prices=[
            LabeledPrice(
                label='access to secret information',
                amount=99000
            ),
            LabeledPrice(
                label='VAT',
                amount=20000
            ),
            LabeledPrice(
                label='Discount',
                amount=-20000
            ),
            LabeledPrice(
                label='Bonus',
                amount=-40000
            )
        ],
        max_tip_amount=20000,
        suggested_tip_amounts=[500, 1500, 5000, 15000],
        start_parameter='',
        provider_data=None,
        photo_url='E:\PET-PROJECTS\AutoSocial\sticker-image-AgADuDkAAg2rsUs.png',
        photo_size=100,
        photo_width=800,
        photo_height=450,
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
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


async def successful_payment(message:Message):
    msg = f'Thank you ofr payment {message.successful_payment.total_amount // 100} {message.successful_payment.currency}. ' \
          f'\r\nYou can download digital version of our product https://google.com'
    await message.answer(msg)
