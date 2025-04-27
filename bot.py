import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

import os

# Получаем токен из переменных окружения
TOKEN = os.getenv("7770466925: AAF1vtWtw8x—6cABnhDG2
P3i7nw0PGxvzds")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я работаю!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ты сказал: {update.message.text}")


async def main():
    if not TOKEN:
        print("Ошибка: токен не найден. Убедись, что TELEGRAM_TOKEN задан в настройках окружения.")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Бот запущен...")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
