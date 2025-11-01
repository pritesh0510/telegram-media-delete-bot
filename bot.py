
import os
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Delete after 5 hours (18000 seconds)
DELETE_DELAY = 18000

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def delete_media(context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.delete_message(chat_id=context.job.chat_id, message_id=context.job.message_id)
    except Exception as e:
        print(f"Failed to delete message: {e}")

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.photo or message.video:
        context.job_queue.run_once(delete_media, DELETE_DELAY, chat_id=message.chat_id, name=str(message.message_id), message_id=message.message_id)
        print(f"Scheduled delete for message {message.message_id}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, handle_media))
    print("🚀 Bot started. Monitoring photos and videos...")
    app.run_polling()
