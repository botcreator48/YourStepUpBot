import logging
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import openai
import httpx

# Настройки
TELEGRAM_TOKEN = "ТВОЙ_ТОКЕН"
OPENAI_API_KEY = "ТВОЙ_OPENAI_КЛЮЧ"

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Установка токена OpenAI
openai.api_key = OPENAI_API_KEY

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    logger.info(f"Новое сообщение: {user_message}")
    try:
        client = openai.AsyncOpenAI()
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты дружелюбный психолог."},
                {"role": "user", "content": user_message},
            ]
        )
        reply_text = response.choices[0].message.content.strip()
        await update.message.reply_text(reply_text)
    except Exception as e:
        logger.error(f"Ошибка при запросе к OpenAI: {e}")
        await update.message.reply_text("Извините, произошла ошибка. Попробуйте позже.")

# Основная функция
async def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    await application.run_polling()

# Запуск
if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
