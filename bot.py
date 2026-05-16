from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import asyncio

TOKEN = "8859950664:AAFQkhUDQi0sgTYWLxgFHPKniX1PAMUhiUA"

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍔 Бургеры")],
        [KeyboardButton(text="🌯 Лаваши")],
        [KeyboardButton(text="🌭 Хот-Доги")],
        [KeyboardButton(text="🍟 Картошка-Фри")],
        [KeyboardButton(text="🥤 Напитки")]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start(message: Message):
    text = """
Здравствуйте дорогой клиент ❤️

Добро пожаловать в Digar-Dog 🌭

Что вы хотите заказать?
"""
    await message.answer(text, reply_markup=menu)

@dp.message(F.text == "🍔 Бургеры")
async def burgers(message: Message):
    text = """
🍔 БУРГЕРЫ

• Чикен Бургер — 20 сомони
• Стрит Бургер — 20 сомони
"""
    await message.answer(text)

@dp.message(F.text == "🌯 Лаваши")
async def lavash(message: Message):
    text = """
🌯 ЛАВАШИ

• Лаваш Махсус — 35 сомони
• Лаваш Плюс — 30 сомони
• Лавашма — 18 / 22 / 30 сомони
"""
    await message.answer(text)

@dp.message(F.text == "🌭 Хот-Доги")
async def hotdog(message: Message):
    text = """
🌭 ХОТ-ДОГИ

• Нондоги Ассорти — 30 / 40 / 50
• Нондоги Мурғи — 18 / 22 / 30
• Чиз-Дог — 30
• Хотдог Супер — 15 / 25
"""
    await message.answer(text)

@dp.message(F.text == "🍟 Картошка-Фри")
async def fries(message: Message):
    text = """
🍟 ФАСТФУД

• Картошка Фри — 10 сомони
• Наггетси — 10 сомони
• Стрипси — 9 сомони
"""
    await message.answer(text)

@dp.message(F.text == "🥤 Напитки")
async def drinks(message: Message):
    text = """
🥤 НАПИТКИ

RC COLA
• 0.5л — 6 сомони
• 1л — 10 сомони
• 1.5л — 11 сомони

RC COLA GREEN
• 0.5л — 6 сомони
• 1л — 10 сомони
• 1.5л — 11 сомони

FANTA
• 0.6л — 6 сомони
• 2л — 13 сомони

FUSETEA ПЕРСИК
• 0.6л — 6 сомони
• 1л — 10 сомони

FUSETEA ЛИМОН
• 0.6л — 6 сомони
• 1л — 10 сомони

SPRITE
• 1л — 11 сомони
"""
    await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())