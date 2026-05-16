from aiogram import Bot, Dispatcher, types, F
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

menu_keyboard = ReplyKeyboardMarkup(
keyboard=[
[KeyboardButton(text="🍔 Бургеры")],
[KeyboardButton(text="🌭 Хот-Доги")],
[KeyboardButton(text="🌯 Лаваш")],
[KeyboardButton(text="🍟 Фри и Закуски")],
[KeyboardButton(text="🥤 Напитки")]
],
resize_keyboard=True
)

@dp.message(CommandStart())
async def start(message: Message):
text = """
👋 <b>Здравствуйте дорогой клиент!</b>

Добро пожаловать в <b>Digar-Dog</b> 🌭🍔

Что вы хотите заказать?
"""
await message.answer(text, reply_markup=menu_keyboard)

@dp.message(F.text == "🍔 Бургеры")
async def burgers(message: Message):
text = """
🍔 <b>БУРГЕРЫ</b>

1. Чикен Бургер — 20 смн
2. Стрит Бургер — 20 смн
3. Чиз-Дог — 30 смн
   """
   await message.answer(text)

@dp.message(F.text == "🌭 Хот-Доги")
async def hotdogs(message: Message):
text = """
🌭 <b>ХОТ-ДОГИ</b>

• Хотдоги Дастрас — 12 смн
• Хотдог Супер — 15 / 25 смн
• Нондоги Мурғи — 18 / 22 / 30 смн
• Нондоги Канадави — 15 / 20 / 25 смн
• Нондоги Анъанави — 13 / 16 / 20 смн
• Нондог Ассорти — 30 / 40 / 50 смн
"""
await message.answer(text)

@dp.message(F.text == "🌯 Лаваш")
async def lavash(message: Message):
text = """
🌯 <b>ЛАВАШ</b>

• Лавашма — 18 / 22 / 30 смн
• Лаваш Кавурдог — 30 / 40 / 50 смн
• Лаваш Плюс — 30 смн
• Лаваш Махсус — 35 смн
"""
await message.answer(text)

@dp.message(F.text == "🍟 Фри и Закуски")
async def fries(message: Message):
text = """
🍟 <b>ФРИ И ЗАКУСКИ</b>

• Картошка Фри — 10 смн
• Наггетси — 10 смн
• Стрипси — 9 смн
• Мургпора — 13 смн
• Мургпора + Фри — 25 смн
• Ассорти (Мургпора) — 35 смн
"""
await message.answer(text)

@dp.message(F.text == "🥤 Напитки")
async def drinks(message: Message):
text = """
🥤 <b>НАПИТКИ</b>

RC COLA
• 0.5л — 6 смн
• 1л — 10 смн
• 1.5л — 11 смн

RC COLA GREEN
• 0.5л — 6 смн
• 1л — 10 смн
• 1.5л — 11 смн

FANTA
• 0.6л — 6 смн
• 2л — 13 смн

FUSETEA ПЕРСИК
• 0.6л — 6 смн
• 1л — 10 смн

FUSETEA ЛИМОН
• 0.6л — 6 смн
• 1л — 10 смн

SPRITE
• 1л — 11 смн
"""
await message.answer(text)

async def main():
await dp.start_polling(bot)

if **name** == "**main**":
asyncio.run(main())
