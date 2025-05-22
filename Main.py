import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Токен бота
TELEGRAM_BOT_TOKEN = '7630163699:AAEPrKWK_r7cPH9FTnJJ7-6o0qa8hWCMcx4'


def shorten_url(long_url):
    try:
        endpoint = 'https://clck.ru/--'
        url = (long_url, '?utm_source=sender')
        response = requests.get(
            endpoint,
            params={'url': url}
        )
        if response.status_code == 200 or response.status_code == 201:
            data = response.text
            return data
        else:
            print(f"Ошибка: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
        return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне длинную ссылку, и я сокращу её для тебя.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    long_url = update.message.text.strip()

    if not long_url.startswith(('http://', 'https://')):
        await update.message.reply_text(
            "Пожалуйста, отправьте корректную ссылку (начинающуюся с http:// или https://).")
        return

    short_url = shorten_url(long_url)

    if short_url:
        await update.message.reply_text(f"Ваша сокращённая ссылка: {short_url}")
    else:
        await update.message.reply_text("Не удалось сократить ссылку. Попробуйте позже.")


def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()


if __name__ == '__main__':
    main()
