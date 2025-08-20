import openai
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from fastapi import FastAPI, Request
import uvicorn
import os

# 🔑 Token-дерді Render Variables ішінен аламыз
TELEGRAM_TOKEN = os.getenv("7708725133:AAE0CS9TbuC4YtNqrMjnVFxcpEFOVU9O0UM")
OPENAI_API_KEY = os.getenv("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")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # мыс: https://senin-bot.onrender.com/webhook

openai.api_key = OPENAI_API_KEY

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
app = FastAPI()

# /start командасы
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Сәлем 👋! Мен ChatGPT-пен жұмыс істейтін Telegram ботпын 🤖")

# Хабарламаларға жауап беру
@dp.message()
async def handle_message(message: Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        answer = response["choices"][0]["message"]["content"]
        await message.answer(answer)
    except Exception as e:
        await message.answer(f"⚠️ Қате шықты: {e}")

# 🚀 Бот қосылғанда Webhook орнатамыз
@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

# Telegram-нан хабар қабылдау
@app.post("/webhook")
async def webhook(request: Request):
    update = await request.json()
    await dp.feed_webhook_update(bot, update)
    return {"ok": True}

# Render uvicorn арқылы іске қосады
if __name__ == "__main__":
    uvicorn.run("bot:app", host="0.0.0.0", port=10000)
