import asyncio
import random

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage


# =====================================
# TOKEN
# =====================================

TOKEN = "8859950664:AAFmAccWOEDB2Zms8YQaf77b8Y2n4zXKBoc"

# ID АДМИНА
ADMIN_ID = 6936232244


# =====================================
# BOT
# =====================================

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher(storage=MemoryStorage())


# =====================================
# MENU
# =====================================

MENU = {
    "🍔 Бургеры": {
        "Чикен Бургер": 20,
        "Стрит Бургер": 20,
    },

    "🌯 Лаваши": {
        "Лаваш Махсус": 35,
        "Лаваш Плюс": 30,
        "Лавашма 18": 18,
        "Лавашма 22": 22,
        "Лавашма 30": 30,
    },

    "🌭 Хот-Доги": {
        "Нондоги Ассорти 30": 30,
        "Нондоги Ассорти 40": 40,
        "Нондоги Ассорти 50": 50,

        "Нондоги Мурғи 18": 18,
        "Нондоги Мурғи 22": 22,
        "Нондоги Мурғи 30": 30,

        "Чиз-Дог": 30,

        "Хотдог Супер 15": 15,
        "Хотдог Супер 25": 25,
    },

    "🍟 Картошка-Фри": {
        "Картошка Фри": 10,
        "Наггетси": 10,
        "Стрипси": 9,
    },

    "🥤 Напитки": {
        "RC COLA 0.5л": 6,
        "RC COLA 1л": 10,
        "RC COLA 1.5л": 11,

        "RC COLA GREEN 0.5л": 6,
        "RC COLA GREEN 1л": 10,
        "RC COLA GREEN 1.5л": 11,

        "FANTA 0.6л": 6,
        "FANTA 2л": 13,

        "FUSETEA ПЕРСИК 0.6л": 6,
        "FUSETEA ПЕРСИК 1л": 10,

        "FUSETEA ЛИМОН 0.6л": 6,
        "FUSETEA ЛИМОН 1л": 10,

        "SPRITE 1л": 11,
    }
}


# =====================================
# STATES
# =====================================

class OrderState(StatesGroup):
    address = State()
    phone = State()
    payment = State()
    waiting_check = State()


# =====================================
# KEYBOARDS
# =====================================

def main_menu():
    buttons = []

    for category in MENU.keys():
        buttons.append([
            InlineKeyboardButton(
                text=category,
                callback_data=f"cat:{category}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="🛒 Корзина",
            callback_data="cart"
        )
    ])

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def products_keyboard(category):
    buttons = []

    for product, price in MENU[category].items():
        buttons.append([
            InlineKeyboardButton(
                text=f"{product} — {price} c",
                callback_data=f"product:{category}:{product}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="back_main"
        )
    ])

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def quantity_keyboard(category, product, qty):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➖",
                    callback_data=f"minus:{category}:{product}:{qty}"
                ),

                InlineKeyboardButton(
                    text=str(qty),
                    callback_data="none"
                ),

                InlineKeyboardButton(
                    text="➕",
                    callback_data=f"plus:{category}:{product}:{qty}"
                ),
            ],

            [
                InlineKeyboardButton(
                    text="🛒 Добавить в корзину",
                    callback_data=f"add:{category}:{product}:{qty}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=f"cat:{category}"
                )
            ]
        ]
    )


def continue_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Да",
                    callback_data="continue_yes"
                )
            ],

            [
                InlineKeyboardButton(
                    text="❌ Нет",
                    callback_data="continue_no"
                )
            ]
        ]
    )


def payment_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💵 Наличные",
                    callback_data="pay:cash"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🏦 Душанбе Сити",
                    callback_data="pay:dushanbe"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📱 Alif",
                    callback_data="pay:alif"
                )
            ]
        ]
    )


def paid_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Оплатил",
                    callback_data="paid"
                )
            ]
        ]
    )


def admin_check_keyboard(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Чек действителен",
                    callback_data=f"accept:{user_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="❌ Чек не действителен",
                    callback_data=f"reject:{user_id}"
                )
            ]
        ]
    )


# =====================================
# START
# =====================================

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "Здравствуйте дорогой клиент ❤️\n\n"
        "Добро пожаловать в Digar-Dog 🌭\n"
        "Что вы хотите заказать?",
        reply_markup=main_menu()
    )


# =====================================
# CATEGORY
# =====================================

@dp.callback_query(F.data.startswith("cat:"))
async def category_handler(callback: CallbackQuery):
    category = callback.data.split(":", 1)[1]

    await callback.message.edit_text(
        f"📂 <b>{category}</b>\n\n"
        f"Выберите товар:",
        reply_markup=products_keyboard(category)
    )

    await callback.answer()


@dp.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "🍽 Главное меню",
        reply_markup=main_menu()
    )

    await callback.answer()


# =====================================
# PRODUCT
# =====================================

@dp.callback_query(F.data.startswith("product:"))
async def product_handler(callback: CallbackQuery):
    _, category, product = callback.data.split(":", 2)

    await callback.message.edit_text(
        f"🛍 {product}\n\n"
        f"Выберите количество:",
        reply_markup=quantity_keyboard(category, product, 1)
    )

    await callback.answer()


# =====================================
# PLUS
# =====================================

@dp.callback_query(F.data.startswith("plus:"))
async def plus_handler(callback: CallbackQuery):
    _, category, product, qty = callback.data.split(":", 3)

    qty = int(qty) + 1

    await callback.message.edit_reply_markup(
        reply_markup=quantity_keyboard(
            category,
            product,
            qty
        )
    )

    await callback.answer()


# =====================================
# MINUS
# =====================================

@dp.callback_query(F.data.startswith("minus:"))
async def minus_handler(callback: CallbackQuery):
    _, category, product, qty = callback.data.split(":", 3)

    qty = max(1, int(qty) - 1)

    await callback.message.edit_reply_markup(
        reply_markup=quantity_keyboard(
            category,
            product,
            qty
        )
    )

    await callback.answer()


# =====================================
# ADD TO CART
# =====================================

@dp.callback_query(F.data.startswith("add:"))
async def add_to_cart(callback: CallbackQuery, state: FSMContext):
    _, category, product, qty = callback.data.split(":", 3)

    qty = int(qty)

    price = MENU[category][product]

    data = await state.get_data()

    cart = data.get("cart", [])

    cart.append({
        "product": product,
        "qty": qty,
        "price": price,
        "total": price * qty
    })

    await state.update_data(cart=cart)

    await callback.message.answer(
        f"✅ {product} x{qty} добавлен в корзину"
    )

    await callback.message.answer(
        "Хотите заказать что-нибудь ещё?",
        reply_markup=continue_keyboard()
    )

    await callback.answer()


# =====================================
# CONTINUE
# =====================================

@dp.callback_query(F.data == "continue_yes")
async def continue_yes(callback: CallbackQuery):
    await callback.message.answer(
        "🍽 Выберите категорию:",
        reply_markup=main_menu()
    )

    await callback.answer()


@dp.callback_query(F.data == "continue_no")
async def continue_no(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.address)

    await callback.message.answer(
        "📍 Введите адрес доставки:"
    )

    await callback.answer()


# =====================================
# ADDRESS
# =====================================

@dp.message(OrderState.address)
async def address_handler(message: Message, state: FSMContext):
    await state.update_data(address=message.text)

    await state.set_state(OrderState.phone)

    await message.answer(
        "📞 Введите номер телефона:"
    )


# =====================================
# PHONE
# =====================================

@dp.message(OrderState.phone)
async def phone_handler(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)

    await state.set_state(OrderState.payment)

    await message.answer(
        "💳 Выберите способ оплаты:",
        reply_markup=payment_keyboard()
    )


# =====================================
# PAYMENT
# =====================================

@dp.callback_query(F.data.startswith("pay:"))
async def payment_handler(callback: CallbackQuery, state: FSMContext):
    payment_method = callback.data.split(":")[1]

    await state.update_data(payment=payment_method)

    # НАЛИЧНЫЕ
    if payment_method == "cash":

        await callback.message.answer(
            "💵 Оплата после доставки курьером"
        )

        await finish_order(callback.message, state)

        await callback.answer()
        return

    # DUSHANBE CITY
    elif payment_method == "dushanbe":

        await callback.message.answer(
            "🏦 Оплатите на номер:\n"
            "+992202288999",
            reply_markup=paid_keyboard()
        )

    # ALIF
    elif payment_method == "alif":

        await callback.message.answer(
            "📱 Оплатите на номер:\n"
            "+992175279955",
            reply_markup=paid_keyboard()
        )

    await callback.answer()


# =====================================
# PAID BUTTON
# =====================================

@dp.callback_query(F.data == "paid")
async def paid_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.waiting_check)

    await callback.message.answer(
        "📸 Отправьте чек пожалуйста"
    )

    await callback.answer()


# =====================================
# CHECK PHOTO
# =====================================

@dp.message(OrderState.waiting_check, F.photo)
async def check_photo_handler(message: Message, state: FSMContext):

    data = await state.get_data()

    cart = data.get("cart", [])
    address = data.get("address")
    phone = data.get("phone")

    text = "🧾 НОВЫЙ ЗАКАЗ\n\n"

    total_sum = 0

    for item in cart:
        text += (
            f"{item['product']} x{item['qty']} = "
            f"{item['total']} c\n"
        )

        total_sum += item["total"]

    text += (
        f"\n💰 Итого: {total_sum} c\n\n"
        f"📍 Адрес: {address}\n"
        f"📞 Телефон: {phone}\n\n"
        f"👤 @{message.from_user.username}\n"
        f"🆔 {message.from_user.id}"
    )

    await bot.send_photo(
        ADMIN_ID,
        photo=message.photo[-1].file_id,
        caption=text,
        reply_markup=admin_check_keyboard(
            message.from_user.id
        )
    )

    await message.answer(
        "✅ Чек отправлен админу на проверку"
    )


# =====================================
# ACCEPT CHECK
# =====================================

@dp.callback_query(F.data.startswith("accept:"))
async def accept_handler(callback: CallbackQuery):

    user_id = int(
        callback.data.split(":")[1]
    )

    order_id = random.randint(1000, 9999)

    await bot.send_message(
        user_id,
        f"✅ Ваш заказ принят!\n\n"
        f"🚚 Курьер свяжется с вами\n\n"
        f"🧾 ID заказа: #{order_id}"
    )

    await callback.message.edit_caption(
        caption="✅ Чек подтвержден"
    )

    await callback.answer()


# =====================================
# REJECT CHECK
# =====================================

@dp.callback_query(F.data.startswith("reject:"))
async def reject_handler(callback: CallbackQuery):

    user_id = int(
        callback.data.split(":")[1]
    )

    await bot.send_message(
        user_id,
        "❌ Заказ не принят\n\n"
        "Чек недействителен"
    )

    await callback.message.edit_caption(
        caption="❌ Чек отклонен"
    )

    await callback.answer()


# =====================================
# CART
# =====================================

@dp.callback_query(F.data == "cart")
async def cart_handler(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    cart = data.get("cart", [])

    if not cart:
        await callback.message.answer(
            "🛒 Корзина пустая"
        )
        return

    text = "🛒 <b>Корзина:</b>\n\n"

    total_sum = 0

    for item in cart:

        text += (
            f"{item['product']} x{item['qty']} = "
            f"{item['total']} c\n"
        )

        total_sum += item["total"]

    text += f"\n💰 Итого: {total_sum} c"

    await callback.message.answer(text)

    await callback.answer()


# =====================================
# FINISH ORDER
# =====================================

async def finish_order(message: Message, state: FSMContext):

    data = await state.get_data()

    cart = data.get("cart", [])
    address = data.get("address")
    phone = data.get("phone")
    payment = data.get("payment")

    text = "🧾 НОВЫЙ ЗАКАЗ\n\n"

    total_sum = 0

    for item in cart:

        text += (
            f"{item['product']} x{item['qty']} = "
            f"{item['total']} c\n"
        )

        total_sum += item["total"]

    text += (
        f"\n💰 Итого: {total_sum} c\n\n"
        f"📍 Адрес: {address}\n"
        f"📞 Телефон: {phone}\n"
        f"💳 Оплата: {payment}"
    )

    await bot.send_message(
        ADMIN_ID,
        text
    )

    await message.answer(
        "✅ Заказ оформлен!"
    )

    await state.clear()


# =====================================
# RUN
# =====================================

async def main():
    print("BOT STARTED")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())