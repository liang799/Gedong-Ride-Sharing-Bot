from telegram import Update
from telegram.ext import ContextTypes


async def drive_to(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Please share the Google Map URL Location. Example: "
                                    "https://goo.gl/maps/UuEC3fpGAHV9a7K38 ")
