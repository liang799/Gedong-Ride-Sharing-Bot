import re

import requests as requests
from telegram import Update, ReplyKeyboardRemove, InlineQueryResultsButton, WebAppInfo, KeyboardButton, \
    ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from LatLong import LatLong
from MapLocation import MapLocation
from db.potentialpassenger import PotentialPassengerRepository, PotentialPassenger

SELECTING_PASSENGER_DESTINATION = map(chr, range(2))


async def drop_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please share the Google Map URL Location. Example: "
                                    "https://maps.app.goo.gl/UuEC3fpGAHV9a7K38 ")
    return SELECTING_PASSENGER_DESTINATION


def create_selecting_passenger_destination(repository: PotentialPassengerRepository):
    async def selecting_passenger_destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
        location_url = update.message.text
        r = requests.get(location_url)
        raw_location_name = re.search("\/place\/([^\/]+)\/", r.url)
        if raw_location_name is None:
            await update.message.reply_text("Location name not found in the URL")
            return SELECTING_PASSENGER_DESTINATION

        location_name = re.sub("\+", " ", raw_location_name.group(1).strip())

        pattern = r'@(-?\d+\.\d+),(-?\d+\.\d+)'
        lat_long_match = re.search(pattern, r.url)

        if lat_long_match is None:
            await update.message.reply_text("Lat Long not found in URL")
            return SELECTING_PASSENGER_DESTINATION

        latitude = lat_long_match.group(1)
        longitude = lat_long_match.group(2)

        kb = [[
            KeyboardButton("Click here to see list of potential drivers",
                           web_app=WebAppInfo(f"https://example.com/passenger/@{latitude},{longitude}"))
        ]]
        await update.message.reply_text(f"Received location: {location_name} "
                                        f"@{latitude},{longitude}",
                                        reply_markup=ReplyKeyboardMarkup(kb))

        repository.addPassenger(
            PotentialPassenger(
                update.message.from_user.id,
                MapLocation(location_url, location_name, LatLong(latitude, longitude))
            ))

        return ConversationHandler.END
    return selecting_passenger_destination


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text('Bye! Hope to talk to you again soon.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
