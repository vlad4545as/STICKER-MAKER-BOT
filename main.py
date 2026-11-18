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

TOKEN = os.getenv("8898722164:AAGjKmCveWRY_FSgTqY9sCjJ_Q9IFS4l67g")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎨 Привіт! Це Sticker Maker Bot!\n\n"
        "📸 Надішли фотографію — зроблю з неї стікер.\n\n"
        "Команди:\n"
        "/start — головне меню\n"
        "/help — допомога"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📸 Надішли мені фотографію.\n"
        "✂️ Я перетворю її на Telegram-стікер!"
    )

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    try:
        photo = message.photo[-1]
        telegram_file = await context.bot.get_file(photo.file_id)

        original = BytesIO()
        await telegram_file.download_to_memory(out=original)
        original.seek(0)

        image = Image.open(original).convert("RGBA")
        image.thumbnail((512, 512))

        output = BytesIO()

        quality = 90
        while quality >= 30:
            output.seek(0)
            output.truncate(0)

            image.save(
                output,
                format="WEBP",
                quality=quality,
                method=6
            )

            if output.tell() <= 512 * 1024:
                break

            quality -= 10

        if output.tell() > 512 * 1024:
            await message.reply_text("❌ Фото завелике для стікера.")
            return

        output.seek(0)
        output.name = "sticker.webp"

        await message.reply_sticker(sticker=output)

    except Exception:
        logging.exception("Sticker creation error")
        await message.reply_text(
            "❌ Не вдалося створити стікер. Спробуй інше фото."
        )

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN не встановлено!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(
        MessageHandler(filters.PHOTO, photo_handler)
    )

    print("Sticker Maker Bot started!")

    app.run_polling()

if name == "main":
    main()
