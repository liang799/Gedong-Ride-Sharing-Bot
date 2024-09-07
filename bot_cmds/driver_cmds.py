import re

import requests as requests
from telegram import Update, ReplyKeyboardRemove
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from LatLong import LatLong
from MapLocation import MapLocation
from db.potentialpassenger import PotentialPassengerRepository

SELECTING_DRIVER_DESTINATION = map(chr, range(1))


async def drive_to(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please share the Google Map URL Location. Example: "
                                    "https://maps.app.goo.gl/UuEC3fpGAHV9a7K38 ")
    return SELECTING_DRIVER_DESTINATION


def create_selecting_driver_destination(repository: PotentialPassengerRepository):
    async def selecting_driver_destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
        location_url = update.message.text
        try:
            location = MapLocation(location_url)
        except Exception as e:
            exception_message = str(e)
            await update.message.reply_text(f"An error occurred: {exception_message}")
            return ConversationHandler.END

        await update.message.reply_text(f"Received location: {location.location_name} "
                                        f"@{location.lat_long.lat},{location.lat_long.long}")

        """
        TODO: Add code here to
        1. Query list of passengers within range
        2. If list not empty, notify these drivers
        """
        passengers = repository.getListOfPassengersWithin(location.lat_long)
        if not passengers:
            return ConversationHandler.END

        newline = "\n"
        title = "List of existing passengers that have similar destination as yours: \n"
        text = title + newline.join(
            f"{idx + 1}. <a href='{passenger.location.url}'>{passenger.location.location_name}</a>"
            for idx, passenger in enumerate(passengers)
        )

        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
        return ConversationHandler.END

    return selecting_driver_destination


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text('Bye! Hope to talk to you again soon.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
