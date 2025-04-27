from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging

# Вставь сюда свой токен
TOKEN = '7770466925:AAFeUfA4twxJlsSGeNuPk26mrDn-QQBqtE0'

# Настроим логирование (чтобы видеть ошибки/инфу)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Обработчик команды /start
async def start(update, context):
    await update.message.reply_text('Привет! Я бот.')

# Обработчик обычных сообщений
async def echo(update, context):
    await update.message.reply_text(update.message.text)

def main():
    # Создаем приложение
    app = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускаем бота
    app.run_polling()

if __name__ == '__main__':
    main()
