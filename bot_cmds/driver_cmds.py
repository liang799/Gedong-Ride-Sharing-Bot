import re

import requests as requests
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

from LatLong import LatLong
from db.potentialpassenger import PotentialPassengerRepository

SELECTING_DRIVER_DESTINATION = map(chr, range(1))


async def drive_to(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please share the Google Map URL Location. Example: "
                                    "https://maps.app.goo.gl/UuEC3fpGAHV9a7K38 ")
    return SELECTING_DRIVER_DESTINATION


def create_selecting_driver_destination(repository: PotentialPassengerRepository):
    async def selecting_driver_destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
        location_url = update.message.text
        r = requests.get(location_url)
        raw_location_name = re.search("\/place\/([^\/]+)\/", r.url)
        if raw_location_name is None:
            await update.message.reply_text("Location name not found in the URL")
            return SELECTING_DRIVER_DESTINATION

        location_name = re.sub("\+", " ", raw_location_name.group(1).strip())

        pattern = r'@(-?\d+\.\d+),(-?\d+\.\d+)'
        lat_long_match = re.search(pattern, r.url)

        if lat_long_match is None:
            await update.message.reply_text("Lat Long not found in URL")
            return SELECTING_DRIVER_DESTINATION

        latitude = lat_long_match.group(1)
        longitude = lat_long_match.group(2)

        await update.message.reply_text(f"Received location: {location_name} "
                                        f"@{latitude},{longitude}")

        """
        TODO: Add code here to
        1. Query list of passengers within range
        2. If list not empty, notify these drivers
        """
        passengers = repository.getListOfPassengersWithin(LatLong(latitude, longitude))
        if not passengers:
            return ConversationHandler.END

        newline = "\n"
        title = "List of existing users: \n"
        text = title + newline.join(f"{idx}. {passenger.lat_long}" for idx, passenger in enumerate(passengers))

        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        return ConversationHandler.END

    return selecting_driver_destination


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text('Bye! Hope to talk to you again soon.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
