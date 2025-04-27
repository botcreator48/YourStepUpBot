import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я твой помощник. Расскажи, что у тебя на душе.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты доброжелательный и решительный психолог-помощник. Помоги человеку разобраться в себе и найти мотивацию двигаться вперёд."},
            {"role": "user", "content": user_message}
        ]
    )

    reply_text = response['choices'][0]['message']['content']
    await update.message.reply_text(reply_text)

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Бот запущен...")
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
