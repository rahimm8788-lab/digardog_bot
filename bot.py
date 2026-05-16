import asyncio
from uuid import uuid4

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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

pending_checks = {}


class OrderState(StatesGroup):
    choosing = State()
    address = State()
    entrance = State()
    phone = State()
    payment = State()
    paid_confirmation = State()
    check_upload = State()


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
    "cash": "💵 Наличными",
    "dc": "🏦 Душанбе Сити",
    "alif": "🟣 Alif",
}


def main_menu_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=name, callback_data=f"cat:{category_id}")]
        for category_id, name in CATEGORIES.items()
    ]
    rows.append([InlineKeyboardButton(text="🛒 Оформить заказ", callback_data="checkout")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def category_keyboard(category_id: str, cart: dict) -> InlineKeyboardMarkup:
    rows = []
    for product_id, product in PRODUCTS.items():
        if product["category"] != category_id:
            continue

        quantity = cart.get(product_id, 0)
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"{product['name']} — {product['price']} сомони",
                    callback_data="noop",
                )
            ]
        )
        rows.append(
            [
                InlineKeyboardButton(text="➖", callback_data=f"cart:minus:{product_id}"),
                InlineKeyboardButton(text=str(quantity), callback_data="noop"),
                InlineKeyboardButton(text="➕", callback_data=f"cart:plus:{product_id}"),
            ]
        )

    rows.append([InlineKeyboardButton(text="⬅️ Категории", callback_data="menu")])
    rows.append([InlineKeyboardButton(text="🛒 Оформить заказ", callback_data="checkout")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def payment_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💵 Наличными", callback_data="pay:cash")],
            [InlineKeyboardButton(text="🏦 Душанбе Сити", callback_data="pay:dc")],
            [InlineKeyboardButton(text="🟣 Alif", callback_data="pay:alif")],
        ]
    )


def paid_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Оплатил", callback_data="paid")],
        ]
    )


def admin_check_keyboard(check_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Чек действителен",
                    callback_data=f"check:valid:{check_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Чек не действителен",
                    callback_data=f"check:invalid:{check_id}",
                )
            ],
        ]
    )


def cart_total(cart: dict) -> int:
    return sum(PRODUCTS[product_id]["price"] * quantity for product_id, quantity in cart.items())


def cart_text(cart: dict) -> str:
    if not cart:
        return "🛒 Корзина пустая."

    lines = ["🛒 Ваш заказ:"]
    for product_id, quantity in cart.items():
        product = PRODUCTS[product_id]
        lines.append(
            f"• {product['name']} x {quantity} = {product['price'] * quantity} сомони"
        )
    lines.append(f"\nИтого: {cart_total(cart)} сомони")
    return "\n".join(lines)


def order_summary(data: dict) -> str:
    return (
        f"{cart_text(data.get('cart', {}))}\n\n"
        f"📍 Адрес: {data.get('address')}\n"
        f"🏢 Подъезд: {data.get('entrance')}\n"
        f"📞 Телефон: {data.get('phone')}\n"
        f"💳 Оплата: {data.get('payment')}"
    )


async def ensure_cart(state: FSMContext) -> dict:
    data = await state.get_data()
    cart = data.get("cart")
    if cart is None:
        cart = {}
        await state.update_data(cart=cart)
    return cart


async def show_main_menu(message: types.Message, state: FSMContext):
    await state.set_state(OrderState.choosing)
    await message.answer(
        "Здравствуйте дорогой клиент 👋\n"
        "Добро пожаловать в Digar-Dog 🌭\n"
        "Что вы хотите заказать?",
        reply_markup=main_menu_keyboard(),
    )


@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await state.update_data(cart={})
    await show_main_menu(message, state)


@dp.callback_query(F.data == "menu")
async def menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.choosing)
    await callback.message.edit_text(
        "Что вы хотите заказать?",
        reply_markup=main_menu_keyboard(),
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("cat:"))
async def category_callback(callback: types.CallbackQuery, state: FSMContext):
    category_id = callback.data.split(":", maxsplit=1)[1]
    if category_id not in CATEGORIES:
        await callback.answer("Категория не найдена.", show_alert=True)
        return

    cart = await ensure_cart(state)
    await state.set_state(OrderState.choosing)
    await state.update_data(current_category=category_id)
    await callback.message.edit_text(
        f"{CATEGORIES[category_id]}\n\nВыберите количество товара:",
        reply_markup=category_keyboard(category_id, cart),
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("cart:"))
async def change_cart_callback(callback: types.CallbackQuery, state: FSMContext):
    _, action, product_id = callback.data.split(":", maxsplit=2)
    if product_id not in PRODUCTS:
        await callback.answer("Товар не найден.", show_alert=True)
        return

    data = await state.get_data()
    cart = data.get("cart", {})

    if action == "plus":
        cart[product_id] = cart.get(product_id, 0) + 1
        answer_text = "✅ Товар добавлен в корзину."
    elif action == "minus":
        if cart.get(product_id, 0) > 1:
            cart[product_id] -= 1
        else:
            cart.pop(product_id, None)
        answer_text = "Количество изменено."
    else:
        await callback.answer()
        return

    category_id = PRODUCTS[product_id]["category"]
    await state.update_data(cart=cart, current_category=category_id)
    await callback.message.edit_text(
        f"{answer_text}\nХотите заказать что-нибудь ещё?\n\n{CATEGORIES[category_id]}",
        reply_markup=category_keyboard(category_id, cart),
    )
    await callback.answer(answer_text)


@dp.callback_query(F.data == "checkout")
async def checkout_callback(callback: types.CallbackQuery, state: FSMContext):
    cart = await ensure_cart(state)
    if not cart:
        await callback.answer("Корзина пустая.", show_alert=True)
        return

    await state.set_state(OrderState.address)
    await callback.message.edit_text(
        f"{cart_text(cart)}\n\n📍 Введите адрес доставки"
    )
    await callback.answer()


@dp.message(OrderState.address, F.text)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text.strip())
    await state.set_state(OrderState.entrance)
    await message.answer("🏢 Укажите подъезд")


@dp.message(OrderState.entrance, F.text)
async def get_entrance(message: types.Message, state: FSMContext):
    await state.update_data(entrance=message.text.strip())
    await state.set_state(OrderState.phone)
    await message.answer("📞 Введите номер телефона")


@dp.message(OrderState.phone, F.text)
async def get_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await state.set_state(OrderState.payment)
    await message.answer("💳 Выберите способ оплаты", reply_markup=payment_keyboard())


@dp.callback_query(OrderState.payment, F.data.startswith("pay:"))
async def payment_callback(callback: types.CallbackQuery, state: FSMContext):
    payment_id = callback.data.split(":", maxsplit=1)[1]
    if payment_id not in PAYMENTS:
        await callback.answer("Выберите способ оплаты.", show_alert=True)
        return

    await state.update_data(payment=PAYMENTS[payment_id])

    if payment_id == "cash":
        await callback.message.edit_text(
            "💵 Оплата наличными при получении заказа.\n\n"
            "✅ Заказ принят.\n"
            "🚚 Ожидайте заказ, курьер свяжется с вами."
        )
        await callback.answer()
        await state.clear()
        return

    await state.set_state(OrderState.paid_confirmation)
    if payment_id == "dc":
        text = f"💳 Оплатите на номер Душанбе Сити:\n{DUSHANBE_CITY_PHONE}"
    else:
        text = f"💳 Оплатите на номер Alif:\n{ALIF_PHONE}"

    await callback.message.edit_text(text, reply_markup=paid_keyboard())
    await callback.answer()


@dp.callback_query(OrderState.paid_confirmation, F.data == "paid")
async def paid_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.check_upload)
    await callback.message.edit_text("📸 Отправьте чек пожалуйста")
    await callback.answer()


@dp.message(OrderState.check_upload, F.photo)
async def check_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user = message.from_user
    username = f"@{user.username}" if user and user.username else "без username"
    full_name = user.full_name if user else "не указан"
    check_id = uuid4().hex[:12]
    caption = (
        "🧾 Новый чек на проверку\n\n"
        f"{order_summary(data)}\n\n"
        f"Клиент: {full_name} ({username})"
    )

    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=message.photo[-1].file_id,
        caption=caption,
        reply_markup=admin_check_keyboard(check_id),
    )

    pending_checks[check_id] = {
        "client_chat_id": message.chat.id,
    }

    await message.answer("✅ Чек отправлен на проверку.")
    await state.clear()


@dp.message(OrderState.check_upload)
async def wrong_check(message: types.Message):
    await message.answer("Пожалуйста, отправьте чек фотографией.")


@dp.callback_query(F.data.startswith("check:"))
async def admin_check_callback(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Эти кнопки доступны только администратору.", show_alert=True)
        return

    _, action, check_id = callback.data.split(":", maxsplit=2)
    check = pending_checks.pop(check_id, None)
    if not check:
        await callback.answer("Чек уже обработан.", show_alert=True)
        return

    if action == "valid":
        client_text = "✅ Заказ принят.\n🚚 Ожидайте заказ, курьер свяжется с вами."
        admin_answer = "Чек подтвержден."
    else:
        client_text = "❌ Чек не действителен.\nЗаказ не принят."
        admin_answer = "Чек отклонен."

    await bot.send_message(chat_id=check["client_chat_id"], text=client_text)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer(admin_answer)


@dp.callback_query(F.data == "noop")
async def noop_callback(callback: types.CallbackQuery):
    await callback.answer()


@dp.message(StateFilter(None))
async def unknown_message(message: types.Message, state: FSMContext):
    await state.update_data(cart={})
    await show_main_menu(message, state)


@dp.callback_query()
async def unknown_callback(callback: types.CallbackQuery):
    await callback.answer("Нажмите /start, чтобы начать новый заказ.", show_alert=True)


async def main():
    await bot.set_my_description(BOT_DESCRIPTION)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
