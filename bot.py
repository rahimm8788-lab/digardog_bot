import asyncio

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "8859950664:AAFQkhUDQi0sgTYWLxgFHPKniX1PAMUhiUA"
BOT_DESCRIPTION = (
    "🍔 Digar Dog — быстрая доставка фастфуда\n\n"
    "📞 Связь с оператором:\n"
    "@rahimovv03\n"
    "+992922002122"
)

bot = Bot(token=TOKEN)
dp = Dispatcher()


class OrderState(StatesGroup):
    choosing = State()
    waiting_for_address = State()
    waiting_for_phone = State()
    waiting_for_payment = State()


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
    "cash": "Наличными",
    "card": "Картой",
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
            [InlineKeyboardButton(text="Наличными", callback_data="pay:cash")],
            [InlineKeyboardButton(text="Картой", callback_data="pay:card")],
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
        "✅ Заказ оформлен.\n\n"
        f"{cart_text(data.get('cart', {}))}\n\n"
        f"📍 Адрес: {data.get('address')}\n"
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
        await callback.answer("✅ Товар добавлен в корзину.")
    elif action == "minus":
        if cart.get(product_id, 0) > 1:
            cart[product_id] -= 1
        else:
            cart.pop(product_id, None)
        await callback.answer("Количество изменено.")
    else:
        await callback.answer()
        return

    category_id = PRODUCTS[product_id]["category"]
    await state.update_data(cart=cart, current_category=category_id)
    await callback.message.edit_text(
        "✅ Товар добавлен в корзину.\n"
        "Хотите заказать что-нибудь ещё?\n\n"
        f"{CATEGORIES[category_id]}",
        reply_markup=category_keyboard(category_id, cart),
    )


@dp.callback_query(F.data == "checkout")
async def checkout_callback(callback: types.CallbackQuery, state: FSMContext):
    cart = await ensure_cart(state)
    if not cart:
        await callback.answer("Корзина пустая.", show_alert=True)
        return

    await state.set_state(OrderState.waiting_for_address)
    await callback.message.edit_text(
        f"{cart_text(cart)}\n\n📍 Введите адрес доставки"
    )
    await callback.answer()


@dp.message(OrderState.waiting_for_address, F.text)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text.strip())
    await state.set_state(OrderState.waiting_for_phone)
    await message.answer("📞 Введите номер телефона")


@dp.message(OrderState.waiting_for_phone, F.text)
async def get_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await state.set_state(OrderState.waiting_for_payment)
    await message.answer("💳 Выберите способ оплаты", reply_markup=payment_keyboard())


@dp.callback_query(OrderState.waiting_for_payment, F.data.startswith("pay:"))
async def payment_callback(callback: types.CallbackQuery, state: FSMContext):
    payment_id = callback.data.split(":", maxsplit=1)[1]
    if payment_id not in PAYMENTS:
        await callback.answer("Выберите способ оплаты.", show_alert=True)
        return

    await state.update_data(payment=PAYMENTS[payment_id])
    data = await state.get_data()
    await callback.message.edit_text(order_summary(data))
    await callback.answer("Заказ оформлен.")
    await state.clear()


@dp.callback_query(F.data == "noop")
async def noop_callback(callback: types.CallbackQuery):
    await callback.answer()


@dp.message(StateFilter(None))
async def unknown_message(message: types.Message, state: FSMContext):
    await state.update_data(cart={})
    await show_main_menu(message, state)


@dp.callback_query()
async def unknown_callback(callback: types.CallbackQuery):
    await callback.answer("Кнопка уже не активна.", show_alert=True)


async def main():
    await bot.set_my_description(BOT_DESCRIPTION)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
