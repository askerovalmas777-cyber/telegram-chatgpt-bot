import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
import openai
from dotenv import load_dotenv

load_dotenv()

# Лог
logging.basicConfig(level=logging.INFO)

# Telegram Bot токен
API_TOKEN = os.getenv("7708725133:AAE0CS9TbuC4YtNqrMjnVFxcpEFOVU9O0UM")
# OpenAI API кілті
openai.api_key = os.getenv("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")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    await message.answer("Сәлем! Мен ChatGPT-пен жұмыс істейтін ботпын 🤖. Маған хабарлама жаз.")

@dp.message_handler()
async def echo(message: Message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message.text}]
    )
    reply = response["choices"][0]["message"]["content"]
    await message.answer(reply)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
