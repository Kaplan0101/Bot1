import os
import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher()

app = FastAPI()

# Telegram webhook endpoint
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update(**data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}

# Basit /start komutu
@dp.message(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("✅ Bot çalışıyor! Webhook başarıyla kuruldu.")

# Uygulama başlatılırken webhook ayarla
@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook set: {WEBHOOK_URL}")

# Uygulama kapanırken webhook kaldır
@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
