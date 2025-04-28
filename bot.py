import logging
import os
import openai
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Включаем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Устанавливаем API ключи
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Приветственное сообщение
WELCOME_MESSAGE = (
    "Привет! Я твой личный ИИ-психолог, помощник и просто хороший собеседник. "
    "Здесь ты можешь спокойно задать любой вопрос — я рядом и всегда готов поддержать тебя."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    logger.info(f"Новое сообщение: {user_message}")

    try:
        response = await asyncio.to_thread(
            openai.chat.completions.create,
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты дружелюбный психолог и собеседник."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response.choices[0].message.content.strip()
        await update.message.reply_text(bot_reply)

    except Exception as e:
        logger.error(f"Ошибка при запросе к OpenAI: {e}")
        await update.message.reply_text("Извините, произошла ошибка. Попробуйте позже.")

async def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен.")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
