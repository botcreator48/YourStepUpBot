import logging
import os
import openai
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получение токенов из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверка токенов
if not TELEGRAM_TOKEN:
    raise ValueError("Переменная окружения TELEGRAM_TOKEN не установлена")
if not OPENAI_API_KEY:
    raise ValueError("Переменная окружения OPENAI_API_KEY не установлена")

# Установка ключа OpenAI
openai.api_key = OPENAI_API_KEY

# Приветственное сообщение
WELCOME_MESSAGE = "Привет! Я твой личный ИИ-психолог, помощник и просто хороший собеседник. Здесь ты можешь спокойно задать любой вопрос — я рядом и всегда готов поддержать тебя."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(}")

    try:
        response = await ask_openai(user_message)
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Ошибка при запросе к OpenAI: {e}")
        await update.message.reply_text("Извините, произошла ошибка. Попробуйте позже.")

async def ask_openai(prompt: str) -> str:
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "syst", "content": "Ты — заботливый и понимающий психолог."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=500,
    )
    return response['choices'][0]['message']['content'].strip()

async def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
