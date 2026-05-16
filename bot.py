import asyncio
import random
from uuid import uuid4

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

TOKEN = "8859950664:AAFQkhUDQi0sgTYWLxgFHPKniX1PAMUhiUA"
ADMIN_ID = 6936232244
BOT_DESCRIPTION = (
    "🍔 Digar Dog — быстрая доставка фастфуда\n\n"
    "📞 Связь с оператором:\n"
    "@rahimovv03\n"
    "+992922002122"
)

DUSHANBE_CITY_PHONE = "+992202288999"
ALIF_PHONE = "175279955"

bot = Bot(token=TOKEN)
dp = Dispatcher()

pending_checks: dict[str, dict[str, str | int]] = {}


class OrderState(StatesGroup):
    choosing = State()
    address = State()
    entrance = State()
    phone = State()
    payment = State()
    paid_confirmation = State()
    waiting_check = State()


CATEGORIES = {
    "burgers": "🍔 Бургеры",
    "lavash": "🌯 Лаваши",
    "hotdogs": "🌭 Хот-Доги",
    "fries": "🍟 Картошка-Фри",
    "drinks": "🥤 Напитки",
}

PRODUCTS = {
    "chicken_burger": {"category": "burgers", "name": "🍔 Чикен Бургер", "price": 20},
    "street_burger": {"category": "burgers", "name": "🍔 Стрит Бургер", "price": 20},
    "lavash_maxsus": {"category": "lavash", "name": "🌯 Лаваш Махсус", "price": 35},
    "lavash_plus": {"category": "lavash", "name": "🌯 Лаваш Плюс", "price": 30},
    "lavashma_18": {"category": "lavash", "name": "🌯 Лавашма 18", "price": 18},
    "lavashma_22": {"category": "lavash", "name": "🌯 Лавашма 22", "price": 22},
    "lavashma_30": {"category": "lavash", "name": "🌯 Лавашма 30", "price": 30},
    "nondogi_assorti_30": {"category": "hotdogs", "name": "🌭 Нондоги Ассорти 30", "price": 30},
    "nondogi_assorti_40": {"category": "hotdogs", "name": "🌭 Нондоги Ассорти 40", "price": 40},
    "nondogi_assorti_50": {"category": "hotdogs", "name": "🌭 Нондоги Ассорти 50", "price": 50},
    "nondogi_murgi_18": {"category": "hotdogs", "name": "🌭 Нондоги Мурғи 18", "price": 18},
    "nondogi_murgi_22": {"category": "hotdogs", "name": "🌭 Нондоги Мурғи 22", "price": 22},
    "nondogi_murgi_30": {"category": "hotdogs", "name": "🌭 Нондоги Мурғи 30", "price": 30},
    "cheese_dog": {"category": "hotdogs", "name": "🌭 Чиз-Дог", "price": 30},
    "hotdog_super_15": {"category": "hotdogs", "name": "🌭 Хотдог Супер 15", "price": 15},
    "hotdog_super_25": {"category": "hotdogs", "name": "🌭 Хотдог Супер 25", "price": 25},
    "fries": {"category": "fries", "name": "🍟 Картошка Фри", "price": 10},
    "nuggets": {"category": "fries", "name": "Наггетси", "price": 10},
    "strips": {"category": "fries", "name": "Стрипси", "price": 9},
    "rc_cola_05": {"category": "drinks", "name": "🥤 RC COLA 0.5л", "price": 6},
    "rc_cola_1": {"category": "drinks", "name": "🥤 RC COLA 1л", "price": 10},
    "rc_cola_15": {"category": "drinks", "name": "🥤 RC COLA 1.5л", "price": 11},
    "rc_green_05": {"category": "drinks", "name": "🥤 RC COLA GREEN 0.5л", "price": 6},
    "rc_green_1": {"category": "drinks", "name": "🥤 RC COLA GREEN 1л", "price": 10},
    "rc_green_15": {"category": "drinks", "name": "🥤 RC COLA GREEN 1.5л", "price": 11},
    "fanta_06": {"category": "drinks", "name": "🥤 FANTA 0.6л", "price": 6},
    "fanta_2": {"category": "drinks", "name": "🥤 FANTA 2л", "price": 13},
    "fusetea_peach_06": {"category": "drinks", "name": "🥤 FUSETEA ПЕРСИК 0.6л", "price": 6},
    "fusetea_peach_1": {"category": "drinks", "name": "🥤 FUSETEA ПЕРСИК 1л", "price": 10},
    "fusetea_lemon_06": {"category": "drinks", "name": "🥤 FUSETEA ЛИМОН 0.6л", "price": 6},
    "fusetea_lemon_1": {"category": "drinks", "name": "🥤 FUSETEA ЛИМОН 1л", "price": 10},
    "sprite_1": {"category": "drinks", "name": "🥤 SPRITE 1л", "price": 11},
}

PAYMENTS = {
    "cash": "Наличные",
    "dc": "Dushanbe City",
    "alif": "Alif",
}

PAYMENT_ALIASES = {
    "1": "cash",
    "наличные": "cash",
    "наличными": "cash",
    "cash": "cash",
    "2": "dc",
    "душанбе": "dc",
    "душанбе сити": "dc",
    "dushanbe city": "dc",
    "dc": "dc",
    "3": "alif",
    "алиф": "alif",
    "alif": "alif",
}


def new_session_id() -> str:
    return uuid4().hex[:8]


def new_order_code() -> str:
    return f"{random.randint(1000, 9999)}L"


async def start_new_order(state: FSMContext) -> str:
    await state.clear()
    session_id = new_session_id()
    await state.update_data(session_id=session_id, order_code=new_order_code(), cart={})
    await state.set_state(OrderState.choosing)
    return session_id


async def current_session_id(state: FSMContext) -> str | None:
    data = await state.get_data()
    return data.get("session_id")


async def is_current_session(state: FSMContext, session_id: str) -> bool:
    return await current_session_id(state) == session_id


async def get_cart(state: FSMContext) -> dict[str, int]:
    data = await state.get_data()
    cart = data.get("cart", {})
    return {
        product_id: int(quantity)
        for product_id, quantity in cart.items()
        if product_id in PRODUCTS and int(quantity) > 0
    }


async def save_cart(state: FSMContext, cart: dict[str, int]) -> None:
    clean_cart = {
        product_id: int(quantity)
        for product_id, quantity in cart.items()
        if product_id in PRODUCTS and int(quantity) > 0
    }
    await state.update_data(cart=clean_cart)


def cart_total(cart: dict[str, int]) -> int:
    return sum(PRODUCTS[product_id]["price"] * quantity for product_id, quantity in cart.items())


def cart_text(cart: dict[str, int]) -> str:
    if not cart:
        return "🛒 Корзина пустая."

    lines = ["🛒 Ваш заказ:"]
    for product_id, quantity in cart.items():
        product = PRODUCTS[product_id]
        lines.append(f"• {product['name']} x {quantity} = {product['price'] * quantity} сомони")
    lines.append(f"\nИтого: {cart_total(cart)} сомони")
    return "\n".join(lines)


def order_summary(data: dict) -> str:
    cart = {
        product_id: int(quantity)
        for product_id, quantity in data.get("cart", {}).items()
        if product_id in PRODUCTS and int(quantity) > 0
    }
    return (
        f"🆔 Номер заказа: {data.get('order_code', '-')}\n\n"
        f"{cart_text(cart)}\n\n"
        f"📍 Адрес: {data.get('address', '-')}\n"
        f"🏢 Подъезд/квартира: {data.get('entrance', '-')}\n"
        f"📞 Телефон: {data.get('phone', '-')}\n"
        f"💳 Оплата: {data.get('payment', '-')}"
    )


def main_menu_keyboard(session_id: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=name, callback_data=f"cat:{session_id}:{category_id}")]
        for category_id, name in CATEGORIES.items()
    ]
    rows.append([InlineKeyboardButton(text="🛒 Оформить заказ", callback_data=f"checkout:{session_id}:main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def category_keyboard(session_id: str, category_id: str, cart: dict[str, int]) -> InlineKeyboardMarkup:
    rows = []
    for product_id, product in PRODUCTS.items():
        if product["category"] != category_id:
            continue
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"{product['name']} — {product['price']} сомони",
                    callback_data=f"noop:{session_id}:title:{product_id}",
                )
            ]
        )
        rows.append(
            [
                InlineKeyboardButton(text="➖", callback_data=f"cart:{session_id}:minus:{product_id}"),
                InlineKeyboardButton(text=str(cart.get(product_id, 0)), callback_data=f"noop:{session_id}:qty:{product_id}"),
                InlineKeyboardButton(text="➕", callback_data=f"cart:{session_id}:plus:{product_id}"),
            ]
        )
    rows.append([InlineKeyboardButton(text="⬅️ Категории", callback_data=f"menu:{session_id}:{category_id}")])
    rows.append([InlineKeyboardButton(text="🛒 Оформить заказ", callback_data=f"checkout:{session_id}:{category_id}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def payment_keyboard(session_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Наличные", callback_data=f"pay:{session_id}:cash")],
            [InlineKeyboardButton(text="Dushanbe City", callback_data=f"pay:{session_id}:dc")],
            [InlineKeyboardButton(text="Alif", callback_data=f"pay:{session_id}:alif")],
        ]
    )


def paid_keyboard(session_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Оплатил", callback_data=f"paid:{session_id}")],
        ]
    )


def admin_check_keyboard(check_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Чек действителен", callback_data=f"check:{check_id}:valid")],
            [InlineKeyboardButton(text="❌ Чек не действителен", callback_data=f"check:{check_id}:invalid")],
        ]
    )


def category_text(category_id: str) -> str:
    return (
        f"{CATEGORIES[category_id]}\n\n"
        "Нажмите ➕, чтобы добавить товар.\n"
        "Нажмите ➖, чтобы уменьшить количество."
    )


async def send_main_menu(message: types.Message, state: FSMContext) -> None:
    session_id = await current_session_id(state)
    if not session_id:
        session_id = await start_new_order(state)

    await message.answer(
        "Здравствуйте дорогой клиент 👋\n"
        "Добро пожаловать в Digar-Dog 🌭\n"
        "Что вы хотите заказать?",
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer("Выберите категорию:", reply_markup=main_menu_keyboard(session_id))


async def send_order_to_admin(data: dict, user: types.User | None, title: str) -> None:
    username = f"@{user.username}" if user and user.username else "без username"
    full_name = user.full_name if user else "не указан"
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"{title}\n\n{order_summary(data)}\n\nКлиент: {full_name} ({username})",
    )


async def ask_payment(message: types.Message, state: FSMContext) -> None:
    session_id = await current_session_id(state)
    if not session_id:
        session_id = await start_new_order(state)

    await state.set_state(OrderState.payment)
    await message.answer(
        "💳 Выберите способ оплаты:\n\n"
        "1. Наличные\n"
        "2. Dushanbe City\n"
        "3. Alif",
        reply_markup=payment_keyboard(session_id),
    )


async def accept_cash_order(message: types.Message, state: FSMContext, user: types.User | None) -> None:
    data = await state.get_data()
    await send_order_to_admin(data, user, "💵 Новый заказ с оплатой наличными")
    await message.answer("Оплата наличными при получении заказа")
    await message.answer("✅ Заказ принят")
    await state.clear()


async def send_online_payment(message: types.Message, state: FSMContext, payment_id: str) -> None:
    session_id = await current_session_id(state)
    if not session_id:
        session_id = await start_new_order(state)

    await state.set_state(OrderState.paid_confirmation)
    if payment_id == "dc":
        text = f"Оплатите на номер: {DUSHANBE_CITY_PHONE}"
    else:
        text = f"Оплатите на номер: {ALIF_PHONE}"
    await message.answer(text, reply_markup=paid_keyboard(session_id))


@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await start_new_order(state)
    await send_main_menu(message, state)


@dp.callback_query(OrderState.choosing, F.data.startswith("menu:"))
async def menu_callback(callback: types.CallbackQuery, state: FSMContext):
    parts = callback.data.split(":", maxsplit=2)
    if len(parts) < 2 or not await is_current_session(state, parts[1]):
        await callback.answer()
        return

    await callback.message.edit_text("Выберите категорию:", reply_markup=main_menu_keyboard(parts[1]))
    await callback.answer()


@dp.callback_query(OrderState.choosing, F.data.startswith("cat:"))
async def category_callback(callback: types.CallbackQuery, state: FSMContext):
    parts = callback.data.split(":", maxsplit=2)
    if len(parts) != 3:
        await callback.answer()
        return

    _, session_id, category_id = parts
    if not await is_current_session(state, session_id) or category_id not in CATEGORIES:
        await callback.answer()
        return

    cart = await get_cart(state)
    await state.update_data(current_category=category_id)
    await callback.message.edit_text(
        category_text(category_id),
        reply_markup=category_keyboard(session_id, category_id, cart),
    )
    await callback.answer()


@dp.callback_query(OrderState.choosing, F.data.startswith("cart:"))
async def cart_callback(callback: types.CallbackQuery, state: FSMContext):
    parts = callback.data.split(":", maxsplit=3)
    if len(parts) != 4:
        await callback.answer()
        return

    _, session_id, action, product_id = parts
    if not await is_current_session(state, session_id) or product_id not in PRODUCTS:
        await callback.answer()
        return

    cart = await get_cart(state)
    quantity = cart.get(product_id, 0)

    if action == "plus":
        cart[product_id] = quantity + 1
        notice = f"{PRODUCTS[product_id]['name']} добавлен в корзину"
    elif action == "minus":
        if quantity > 1:
            cart[product_id] = quantity - 1
        else:
            cart.pop(product_id, None)
        notice = f"{PRODUCTS[product_id]['name']} количество изменено"
    else:
        await callback.answer()
        return

    await save_cart(state, cart)
    category_id = PRODUCTS[product_id]["category"]
    await state.update_data(current_category=category_id)
    if action == "plus":
        await callback.message.answer(notice)
    await callback.message.edit_reply_markup(
        reply_markup=category_keyboard(session_id, category_id, cart),
    )
    await callback.answer()


@dp.callback_query(OrderState.choosing, F.data.startswith("checkout:"))
async def checkout_callback(callback: types.CallbackQuery, state: FSMContext):
    parts = callback.data.split(":", maxsplit=2)
    if len(parts) < 2 or not await is_current_session(state, parts[1]):
        await callback.answer()
        return

    cart = await get_cart(state)
    if not cart:
        await callback.message.answer("🛒 Корзина пустая. Добавьте товар перед оформлением.")
        await callback.answer()
        return

    await state.set_state(OrderState.address)
    await callback.message.edit_text(f"{cart_text(cart)}\n\n📍 Введите адрес доставки")
    await callback.answer()


@dp.message(OrderState.address, F.text)
async def address_message(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text.strip())
    await state.set_state(OrderState.entrance)
    await message.answer("🏢 Укажите подъезд/квартиру")


@dp.message(OrderState.address)
async def wrong_address(message: types.Message):
    await message.answer("📍 Введите адрес доставки текстом.")


@dp.message(OrderState.entrance, F.text)
async def entrance_message(message: types.Message, state: FSMContext):
    await state.update_data(entrance=message.text.strip())
    await state.set_state(OrderState.phone)
    await message.answer("📞 Введите номер телефона")


@dp.message(OrderState.entrance)
async def wrong_entrance(message: types.Message):
    await message.answer("🏢 Укажите подъезд/квартиру текстом.")


@dp.message(OrderState.phone, F.text)
async def phone_message(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await ask_payment(message, state)


@dp.message(OrderState.phone)
async def wrong_phone(message: types.Message):
    await message.answer("📞 Введите номер телефона текстом.")


@dp.callback_query(OrderState.payment, F.data.startswith("pay:"))
async def payment_callback(callback: types.CallbackQuery, state: FSMContext):
    parts = callback.data.split(":", maxsplit=2)
    if len(parts) != 3:
        await callback.answer()
        return

    _, session_id, payment_id = parts
    if not await is_current_session(state, session_id) or payment_id not in PAYMENTS:
        await callback.answer()
        return

    await state.update_data(payment=PAYMENTS[payment_id])
    await callback.message.edit_reply_markup(reply_markup=None)
    if payment_id == "cash":
        await accept_cash_order(callback.message, state, callback.from_user)
    else:
        await send_online_payment(callback.message, state, payment_id)
    await callback.answer()


@dp.message(OrderState.payment, F.text)
async def payment_text(message: types.Message, state: FSMContext):
    payment_id = PAYMENT_ALIASES.get(message.text.strip().casefold())
    if payment_id not in PAYMENTS:
        await ask_payment(message, state)
        return

    await state.update_data(payment=PAYMENTS[payment_id])
    if payment_id == "cash":
        await accept_cash_order(message, state, message.from_user)
    else:
        await send_online_payment(message, state, payment_id)


@dp.message(OrderState.payment)
async def wrong_payment(message: types.Message, state: FSMContext):
    await ask_payment(message, state)


@dp.callback_query(OrderState.paid_confirmation, F.data.startswith("paid:"))
async def paid_callback(callback: types.CallbackQuery, state: FSMContext):
    parts = callback.data.split(":", maxsplit=1)
    if len(parts) != 2 or not await is_current_session(state, parts[1]):
        await callback.answer()
        return

    await state.set_state(OrderState.waiting_check)
    await callback.message.edit_text("📸 Отправьте чек оплаты")
    await callback.answer()


@dp.message(OrderState.paid_confirmation)
async def wrong_paid_confirmation(message: types.Message):
    await message.answer("Нажмите кнопку ✅ Оплатил после оплаты.")


@dp.message(OrderState.waiting_check, F.photo)
async def check_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    check_id = uuid4().hex[:12]
    file_id = message.photo[-1].file_id
    user = message.from_user
    username = f"@{user.username}" if user and user.username else "без username"
    full_name = user.full_name if user else "не указан"
    caption = (
        "🧾 Новый чек на проверку\n\n"
        f"{order_summary(data)}\n\n"
        f"Клиент: {full_name} ({username})"
    )

    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=file_id,
        caption=caption,
        reply_markup=admin_check_keyboard(check_id),
    )
    pending_checks[check_id] = {
        "client_chat_id": message.chat.id,
        "order_code": data.get("order_code", "-"),
        "file_id": file_id,
    }

    await message.answer("✅ Чек отправлен на проверку администратору")
    await state.clear()


@dp.message(OrderState.waiting_check)
async def wrong_check(message: types.Message):
    await message.answer("📸 Отправьте чек фотографией.")


@dp.callback_query(F.data.startswith("check:"))
async def admin_check_callback(callback: types.CallbackQuery):
    parts = callback.data.split(":", maxsplit=2)
    if callback.from_user.id != ADMIN_ID or len(parts) != 3:
        await callback.answer()
        return

    _, check_id, action = parts
    check = pending_checks.pop(check_id, None)
    if not check or action not in {"valid", "invalid"}:
        await callback.answer()
        return

    if action == "valid":
        text = (
            "✅ Заказ принят.\n"
            "🚚 Курьер скоро свяжется с вами.\n\n"
            f"🆔 Номер заказа: {check['order_code']}"
        )
    else:
        text = "❌ Чек не действителен.\nЗаказ не принят."

    await bot.send_message(chat_id=int(check["client_chat_id"]), text=text)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()


@dp.callback_query(F.data.startswith("noop:"))
async def noop_callback(callback: types.CallbackQuery):
    await callback.answer()


@dp.callback_query()
async def old_callback(callback: types.CallbackQuery):
    await callback.answer()


@dp.message()
async def fallback_message(message: types.Message, state: FSMContext):
    await start_new_order(state)
    await send_main_menu(message, state)


async def main():
    await bot.set_my_description(BOT_DESCRIPTION)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
