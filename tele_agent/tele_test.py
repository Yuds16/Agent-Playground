from os import getenv
from dotenv import load_dotenv
import asyncio

# Load environment variables from .env file
load_dotenv()

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = getenv("TELEGRAM_BOT_TOKEN", "")

print("Token is:", TELEGRAM_TOKEN)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("hello", hello))

# app.run_polling()


from telegram import Bot

async def test_bot():
    TELEGRAM_TOKEN = getenv("TELEGRAM_BOT_TOKEN", "")
    bot = Bot(token=TELEGRAM_TOKEN)

    try:
        updates = await bot.get_updates()
        messages = [update.message.to_dict() for update in updates if update.message]
        print({"status": "success", "messages": messages})
    except Exception as e:
        print({"status": "error", "message": str(e)})
    finally:
        await bot.close()

# Run the async function
asyncio.run(test_bot())