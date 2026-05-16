from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
import asyncio
from uuid import uuid4

TOKEN = "8859950664:AAFQkhUDQi0sgTYWLxgFHPKniX1PAMUhiUA"
ADMIN_ID = 6936232244
BOT_DESCRIPTION = (
    "🍔 Digar Dog — быстрая доставка фастфуда\n\n"
    "📞 Связь с оператором:\n"
    "@rahimovv03\n"
    "+992922002122"
)

PAYMENT_PHONES = {
    "Alif": "+992175279955",
    "Dushanbe City": "+992202288999",
}

bot = Bot(token=TOKEN)
dp = Dispatcher()

pending_receipts = {}


class OrderState(StatesGroup):
    waiting_for_address = State()
    waiting_for_entrance = State()
    waiting_for_apartment = State()
    waiting_for_phone = State()
    waiting_for_payment = State()
    waiting_for_paid_confirmation = State()
    waiting_for_receipt = State()


FOODS = {
    "🍔 Бургер": 20,
    "🌭 Хот-Дог": 25,
    "🌯 Лаваш": 35,
    "🍟 Картошка Фри": 10,
}

ONLINE_PAYMENTS = {
    "alif": "Alif",
    "dushanbe city": "Dushanbe City",
    "dushanbecity": "Dushanbe City",
}
CASH_PAYMENTS = {"наличные", "cash"}
PAID_BUTTON_TEXT = "✅ Оплатил"

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍔 Бургер")],
        [KeyboardButton(text="🌭 Хот-Дог")],
        [KeyboardButton(text="🌯 Лаваш")],
        [KeyboardButton(text="🍟 Картошка Фри")],
    ],
    resize_keyboard=True,
)

payment_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Наличные")],
        [KeyboardButton(text="Alif")],
        [KeyboardButton(text="Dushanbe City")],
    ],
    resize_keyboard=True,
)

paid_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=PAID_BUTTON_TEXT)]],
    resize_keyboard=True,
)


def receipt_admin_keyboard(receipt_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Чек действителен",
                    callback_data=f"receipt_valid:{receipt_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Чек не действителен",
                    callback_data=f"receipt_invalid:{receipt_id}",
                )
            ],
        ]
    )


@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Добро пожаловать в Digar Dog 🍔",
        reply_markup=menu,
    )


@dp.message(StateFilter(None), F.text)
async def choose_food(message: types.Message, state: FSMContext):
    food_name = message.text.strip()

    if food_name not in FOODS:
        await unknown_message(message)
        return

    price = FOODS[food_name]
    await state.update_data(food=food_name, price=price)
    await state.set_state(OrderState.waiting_for_address)

    await message.answer(
        f"{food_name} стоит {price} сомони\n\n📍 Отправьте адрес доставки.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(OrderState.waiting_for_address)
async def get_address(message: types.Message, state: FSMContext):
    address = message.text.strip() if message.text else ""
    await state.update_data(address=address)
    await state.set_state(OrderState.waiting_for_entrance)
    await message.answer("Укажите подъезд.")


@dp.message(OrderState.waiting_for_entrance)
async def get_entrance(message: types.Message, state: FSMContext):
    entrance = message.text.strip() if message.text else ""
    await state.update_data(entrance=entrance)
    await state.set_state(OrderState.waiting_for_apartment)
    await message.answer("Укажите квартиру.")


@dp.message(OrderState.waiting_for_apartment)
async def get_apartment(message: types.Message, state: FSMContext):
    apartment = message.text.strip() if message.text else ""
    await state.update_data(apartment=apartment)
    await state.set_state(OrderState.waiting_for_phone)
    await message.answer("Укажите номер телефона.")


@dp.message(OrderState.waiting_for_phone)
async def get_phone(message: types.Message, state: FSMContext):
    phone = message.text.strip() if message.text else ""
    await state.update_data(phone=phone)
    await state.set_state(OrderState.waiting_for_payment)
    await message.answer(
        "Выберите способ оплаты:",
        reply_markup=payment_menu,
    )


@dp.message(OrderState.waiting_for_payment)
async def process_payment(message: types.Message, state: FSMContext):
    payment_text = message.text.strip() if message.text else ""
    payment_key = payment_text.casefold()

    if payment_key in CASH_PAYMENTS:
        await state.update_data(payment="Наличные")
        await message.answer("✅ Оплата после доставки.", reply_markup=menu)
        await state.clear()
        return

    if payment_key in ONLINE_PAYMENTS:
        payment_method = ONLINE_PAYMENTS[payment_key]
        payment_phone = PAYMENT_PHONES[payment_method]
        await state.update_data(payment=payment_method)
        await state.set_state(OrderState.waiting_for_paid_confirmation)

        await message.answer(
            f"📱 Оплатите через {payment_method} на номер:\n{payment_phone}",
            reply_markup=paid_menu,
        )
        return

    await message.answer(
        "Пожалуйста, выберите способ оплаты кнопкой ниже.",
        reply_markup=payment_menu,
    )


@dp.message(OrderState.waiting_for_paid_confirmation, F.text)
async def wait_paid_confirmation(message: types.Message, state: FSMContext):
    paid_text = message.text.strip()

    if paid_text == PAID_BUTTON_TEXT:
        await state.set_state(OrderState.waiting_for_receipt)
        await message.answer(
            "📸 Отправьте чек пожалуйста.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return

    await message.answer(
        "Нажмите кнопку «✅ Оплатил» после оплаты.",
        reply_markup=paid_menu,
    )


@dp.message(OrderState.waiting_for_receipt, F.photo)
async def get_receipt_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user = message.from_user
    username = f"@{user.username}" if user and user.username else "без username"
    full_name = user.full_name if user else "не указан"
    address = data.get("address", "не указан")
    entrance = data.get("entrance", "не указан")
    apartment = data.get("apartment", "не указана")
    phone = data.get("phone", "не указан")

    caption = (
        "🧾 Новый чек оплаты\n\n"
        f"Блюдо: {data.get('food', 'не указано')}\n"
        f"Цена: {data.get('price', 'не указана')} сомони\n"
        f"Способ оплаты: {data.get('payment', 'не указан')}\n"
        f"Клиент: {full_name} ({username})\n"
        f"Телефон: {phone}\n"
        f"Адрес: {address}\n"
        f"Подъезд: {entrance}\n"
        f"Квартира: {apartment}"
    )

    receipt_id = uuid4().hex[:12]
    admin_message = await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=message.photo[-1].file_id,
        caption=caption,
        reply_markup=receipt_admin_keyboard(receipt_id),
    )

    checking_message = await message.answer(
        "✅ Чек отправлен на проверку.",
        reply_markup=menu,
    )

    pending_receipts[receipt_id] = {
        "client_chat_id": message.chat.id,
        "checking_message_id": checking_message.message_id,
        "admin_chat_id": admin_message.chat.id,
        "admin_message_id": admin_message.message_id,
    }

    await state.clear()


@dp.message(OrderState.waiting_for_receipt)
async def wrong_receipt(message: types.Message):
    await message.answer("Пожалуйста, отправьте чек фотографией.")


@dp.callback_query(F.data.startswith("receipt_"))
async def process_receipt_callback(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Эта кнопка только для администратора.", show_alert=True)
        return

    action, receipt_id = callback.data.split(":", maxsplit=1)
    receipt = pending_receipts.pop(receipt_id, None)

    if not receipt:
        await callback.answer("Этот чек уже обработан.", show_alert=True)
        return

    try:
        await bot.delete_message(
            chat_id=receipt["client_chat_id"],
            message_id=receipt["checking_message_id"],
        )
    except Exception:
        pass

    if action == "receipt_valid":
        client_text = "✅ Заказ принят. Ждите вызов курьера."
        admin_text = "✅ Чек подтвержден."
    else:
        client_text = "❌ Чек не действителен. Заказ не принят."
        admin_text = "❌ Чек отклонен."

    await bot.send_message(receipt["client_chat_id"], client_text, reply_markup=menu)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer(admin_text)


@dp.message()
async def unknown_message(message: types.Message):
    await message.answer(
        "Выберите блюдо из меню.",
        reply_markup=menu,
    )


async def main():
    await bot.set_my_description(BOT_DESCRIPTION)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
