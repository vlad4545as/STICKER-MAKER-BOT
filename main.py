
import os
import logging
from io import BytesIO
from PIL import Image
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("8898722164:AAE9BygBSzu23UG8zUjUK1JaZj_00VfzlY8")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎨 Привіт! Я Sticker Maker Bot!\n\n"
        "Надішли мені фотографію — і я зроблю з неї стікер.\n\n"
        "Команди:\n"
        "/start — меню\n"
        "/help — допомога"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📸 Надішли фотографію як звичайне фото або файл."
    )

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    photo = message.photo[-1]
    file = await context.bot.get_file(photo.file_id)

    data = BytesIO()
    await file.download_to_memory(out=data)
    data.seek(0)

    image = Image.open(data).convert("RGBA")
    image.thumbnail((512, 512))

    output = BytesIO()
    image.save(output, format="PNG")
    output.seek(0)
    output.name = "sticker.png"

    await message.reply_sticker(sticker=output)

async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is missing")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
