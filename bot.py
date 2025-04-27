import os
import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def generate_response(user_message):
    prompt = f"""
Ты — ИИ-психолог. Помогаешь человеку увидеть свою боль и сделать маленький шаг вперёд. 
Говори по-человечески, честно, иногда дерзко. Короткими абзацами. Заверши ответ сильным вопросом или конкретным предложением действия.

Пользователь написал: "{user_message}"
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response['choices'][0]['message']['content']

def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    response = generate_response(user_message)
    update.message.reply_text(response)

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
