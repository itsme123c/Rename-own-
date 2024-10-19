import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, Filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# In-memory storage for the current name and thumbnail
current_name = ""
current_thumbnail = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Use /rename <new_name> to rename the bot and send a thumbnail image.')

async def rename(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global current_name
    if context.args:
        current_name = " ".join(context.args)
        await update.message.reply_text(f'Bot renamed to: {current_name}')
    else:
        await update.message.reply_text('Please provide a new name. Usage: /rename <new_name>')

async def set_thumbnail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global current_thumbnail
    if update.message.photo:
        photo = update.message.photo[-1].file_id  # Get the highest quality photo
        current_thumbnail = photo
        await update.message.reply_text('Thumbnail set successfully!')

async def show_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global current_name, current_thumbnail
    info = f"Current Name: {current_name or 'Not set'}\n"
    info += f"Current Thumbnail: {'Set' if current_thumbnail else 'Not set'}"
    await update.message.reply_text(info)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rename", rename))
    app.add_handler(MessageHandler(Filters.photo, set_thumbnail))
    app.add_handler(CommandHandler("info", show_info))

    app.run_polling()
