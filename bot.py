import asyncio
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

bot = Bot(token=TOKEN)
dp = Dispatcher()


class OrderState(StatesGroup):
    choosing_category = State()
    choosing_product = State()
    choosing_quantity = State()
    after_cart = State()
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
    "chicken_burger": {"category": "burgers", "name": "Чикен Бургер", "price": 20},
    "street_burger": {"category": "burgers", "name": "Стрит Бургер", "price": 20},
    "lavash_maxsus": {"category": "lavash", "name": "Лаваш Махсус", "price": 35},
    "lavash_plus": {"category": "lavash", "name": "Лаваш Плюс", "price": 30},
    "lavashma_18": {"category": "lavash", "name": "Лавашма 18", "price": 18},
    "lavashma_22": {"category": "lavash", "name": "Лавашма 22", "price": 22},
    "lavashma_30": {"category": "lavash", "name": "Лавашма 30", "price": 30},
    "nondogi_assorti_30": {"category": "hotdogs", "name": "Нондоги Ассорти 30", "price": 30},
    "nondogi_assorti_40": {"category": "hotdogs", "name": "Нондоги Ассорти 40", "price": 40},
    "nondogi_assorti_50": {"category": "hotdogs", "name": "Нондоги Ассорти 50", "price": 50},
    "nondogi_murgi_18": {"category": "hotdogs", "name": "Нондоги Мурғи 18", "price": 18},
    "nondogi_murgi_22": {"category": "hotdogs", "name": "Нондоги Мурғи 22", "price": 22},
    "nondogi_murgi_30": {"category": "hotdogs", "name": "Нондоги Мурғи 30", "price": 30},
    "cheese_dog": {"category": "hotdogs", "name": "Чиз-Дог", "price": 30},
    "hotdog_super_15": {"category": "hotdogs", "name": "Хотдог Супер 15", "price": 15},
    "hotdog_super_25": {"category": "hotdogs", "name": "Хотдог Супер 25", "price": 25},
    "fries": {"category": "fries", "name": "Картошка Фри", "price": 10},
    "nuggets": {"category": "fries", "name": "Наггетси", "price": 10},
    "strips": {"category": "fries", "name": "Стрипси", "price": 9},
    "rc_cola_05": {"category": "drinks", "name": "RC COLA 0.5л", "price": 6},
    "rc_cola_1": {"category": "drinks", "name": "RC COLA 1л", "price": 10},
    "rc_cola_15": {"category": "drinks", "name": "RC COLA 1.5л", "price": 11},
    "rc_green_05": {"category": "drinks", "name": "RC COLA GREEN 0.5л", "price": 6},
    "rc_green_1": {"category": "drinks", "name": "RC COLA GREEN 1л", "price": 10},
    "rc_green_15": {"category": "drinks", "name": "RC COLA GREEN 1.5л", "price": 11},
    "fanta_06": {"category": "drinks", "name": "FANTA 0.6л", "price": 6},
    "fanta_2": {"category": "drinks", "name": "FANTA 2л", "price": 13},
    "fusetea_peach_06": {"category": "drinks", "name": "FUSETEA ПЕРСИК 0.6л", "price": 6},
    "fusetea_peach_1": {"category": "drinks", "name": "FUSETEA ПЕРСИК 1л", "price": 10},
    "fusetea_lemon_06": {"category": "drinks", "name": "FUSETEA ЛИМОН 0.6л", "price": 6},
    "fusetea_lemon_1": {"category": "drinks", "name": "FUSETEA ЛИМОН 1л", "price": 10},
    "sprite_1": {"category": "drinks", "name": "SPRITE 1л", "price": 11},
}

PAYMENTS = {
    "cash": "Наличные",
    "alif": "Alif",
    "dc": "Dushanbe City",
}


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data=f"cat:{category_id}")]
            for category_id, name in CATEGORIES.items()
        ]
    )


def products_keyboard(category_id: str) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text=f"{product['name']} — {product['price']} сомони",
                callback_data=f"product:{product_id}",
            )
        ]
        for product_id, product in PRODUCTS.items()
        if product["category"] == category_id
    ]
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back:categories")])
    rows.append([InlineKeyboardButton(text="🛒 Корзина", callback_data="cart:view")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def quantity_keyboard(quantity: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data="qty:minus"),
                InlineKeyboardButton(text=str(quantity), callback_data="qty:noop"),
                InlineKeyboardButton(text="➕", callback_data="qty:plus"),
            ],
            [InlineKeyboardButton(text="🛒 Добавить в корзину", callback_data="cart:add")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back:products")],
        ]
    )


def after_cart_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да", callback_data="more:yes"),
                InlineKeyboardButton(text="Нет", callback_data="more:no"),
            ],
            [InlineKeyboardButton(text="🛒 Корзина", callback_data="cart:view")],
        ]
    )


def payment_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Наличные", callback_data="pay:cash")],
            [InlineKeyboardButton(text="Alif", callback_data="pay:alif")],
            [InlineKeyboardButton(text="Dushanbe City", callback_data="pay:dc")],
            [InlineKeyboardButton(text="⬅️ Вернуться в меню", callback_data="back:categories")],
        ]
    )


def cart_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Оформить заказ", callback_data="checkout:start")],
            [InlineKeyboardButton(text="⬅️ В меню", callback_data="back:categories")],
        ]
    )


def build_cart_text(cart: dict) -> str:
    if not cart:
        return "🛒 Корзина пустая."

    lines = ["🛒 Ваша корзина:\n"]
    total = 0
    for product_id, quantity in cart.items():
        product = PRODUCTS[product_id]
        item_total = product["price"] * quantity
        total += item_total
        lines.append(f"• {product['name']} x {quantity} = {item_total} сомони")
    lines.append(f"\nИтого: {total} сомони")
    return "\n".join(lines)


def build_order_summary(data: dict) -> str:
    cart = data.get("cart", {})
    summary = build_cart_text(cart)
    return (
        "✅ Заказ оформлен!\n\n"
        f"{summary}\n\n"
        f"📍 Адрес: {data.get('address')}\n"
        f"📞 Телефон: {data.get('phone')}\n"
        f"💳 Оплата: {data.get('payment')}"
    )


async def show_main_menu(target: types.Message | types.CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.choosing_category)
    text = "Что вы хотите заказать?"
    markup = main_menu_keyboard()

    if isinstance(target, types.CallbackQuery):
        await target.message.edit_text(text, reply_markup=markup)
        await target.answer()
    else:
        await target.answer(text, reply_markup=markup)


@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await state.update_data(cart={})
    await message.answer(
        "Здравствуйте дорогой клиент ❤️\n"
        "Добро пожаловать в Digar-Dog 🌭\n"
        "Что вы хотите заказать?",
        reply_markup=main_menu_keyboard(),
    )
    await state.set_state(OrderState.choosing_category)


@dp.callback_query(F.data == "back:categories")
async def back_to_categories(callback: types.CallbackQuery, state: FSMContext):
    await show_main_menu(callback, state)


@dp.callback_query(F.data.startswith("cat:"))
async def choose_category(callback: types.CallbackQuery, state: FSMContext):
    category_id = callback.data.split(":", maxsplit=1)[1]

    if category_id not in CATEGORIES:
        await callback.answer("Категория не найдена.", show_alert=True)
        return

    await state.update_data(category_id=category_id)
    await state.set_state(OrderState.choosing_product)
    await callback.message.edit_text(
        f"{CATEGORIES[category_id]}\n\nВыберите товар:",
        reply_markup=products_keyboard(category_id),
    )
    await callback.answer()


@dp.callback_query(F.data == "back:products")
async def back_to_products(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category_id = data.get("category_id")

    if not category_id:
        await show_main_menu(callback, state)
        return

    await state.set_state(OrderState.choosing_product)
    await callback.message.edit_text(
        f"{CATEGORIES[category_id]}\n\nВыберите товар:",
        reply_markup=products_keyboard(category_id),
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("product:"))
async def choose_product(callback: types.CallbackQuery, state: FSMContext):
    product_id = callback.data.split(":", maxsplit=1)[1]

    if product_id not in PRODUCTS:
        await callback.answer("Товар не найден.", show_alert=True)
        return

    product = PRODUCTS[product_id]
    await state.update_data(selected_product_id=product_id, selected_quantity=1)
    await state.set_state(OrderState.choosing_quantity)
    await callback.message.edit_text(
        f"{product['name']}\nЦена: {product['price']} сомони\n\nВыберите количество:",
        reply_markup=quantity_keyboard(1),
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("qty:"))
async def change_quantity(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split(":", maxsplit=1)[1]
    data = await state.get_data()
    product_id = data.get("selected_product_id")
    quantity = int(data.get("selected_quantity", 1))

    if not product_id:
        await show_main_menu(callback, state)
        return

    if action == "plus":
        quantity += 1
    elif action == "minus":
        quantity = max(1, quantity - 1)
    else:
        await callback.answer()
        return

    product = PRODUCTS[product_id]
    await state.update_data(selected_quantity=quantity)
    await callback.message.edit_text(
        f"{product['name']}\nЦена: {product['price']} сомони\n\nВыберите количество:",
        reply_markup=quantity_keyboard(quantity),
    )
    await callback.answer()


@dp.callback_query(F.data == "cart:add")
async def add_to_cart(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product_id = data.get("selected_product_id")
    quantity = int(data.get("selected_quantity", 1))

    if product_id not in PRODUCTS:
        await callback.answer("Выберите товар заново.", show_alert=True)
        await show_main_menu(callback, state)
        return

    cart = data.get("cart", {})
    cart[product_id] = cart.get(product_id, 0) + quantity
    await state.update_data(cart=cart, selected_product_id=None, selected_quantity=1)
    await state.set_state(OrderState.after_cart)

    product = PRODUCTS[product_id]
    await callback.message.edit_text(
        f"✅ {product['name']} x {quantity} добавлен в корзину.\n\n"
        "Хотите заказать что-нибудь ещё?",
        reply_markup=after_cart_keyboard(),
    )
    await callback.answer()


@dp.callback_query(F.data == "cart:view")
async def view_cart(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(
        build_cart_text(data.get("cart", {})),
        reply_markup=cart_keyboard(),
    )
    await callback.answer()


@dp.callback_query(F.data == "more:yes")
async def order_more(callback: types.CallbackQuery, state: FSMContext):
    await show_main_menu(callback, state)


@dp.callback_query(F.data == "more:no")
@dp.callback_query(F.data == "checkout:start")
async def start_checkout(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("cart"):
        await callback.answer("Корзина пустая.", show_alert=True)
        return

    await state.set_state(OrderState.waiting_for_address)
    await callback.message.edit_text("📍 Напишите адрес доставки:")
    await callback.answer()


@dp.message(OrderState.waiting_for_address, F.text)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text.strip())
    await state.set_state(OrderState.waiting_for_phone)
    await message.answer("📞 Напишите номер телефона:")


@dp.message(OrderState.waiting_for_phone, F.text)
async def get_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await state.set_state(OrderState.waiting_for_payment)
    await message.answer("💳 Выберите способ оплаты:", reply_markup=payment_keyboard())


@dp.callback_query(OrderState.waiting_for_payment, F.data.startswith("pay:"))
async def choose_payment(callback: types.CallbackQuery, state: FSMContext):
    payment_id = callback.data.split(":", maxsplit=1)[1]

    if payment_id not in PAYMENTS:
        await callback.answer("Выберите оплату кнопкой.", show_alert=True)
        return

    await state.update_data(payment=PAYMENTS[payment_id])
    data = await state.get_data()
    await callback.message.edit_text(build_order_summary(data))
    await callback.answer("Заказ оформлен.")
    await state.clear()


@dp.message(StateFilter(None))
async def unknown_message(message: types.Message, state: FSMContext):
    await message.answer(
        "Нажмите /start, чтобы открыть меню заказа.",
        reply_markup=main_menu_keyboard(),
    )
    await state.set_state(OrderState.choosing_category)


@dp.callback_query()
async def unknown_callback(callback: types.CallbackQuery):
    await callback.answer("Эта кнопка уже не активна.", show_alert=True)


async def main():
    await bot.set_my_description(BOT_DESCRIPTION)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
