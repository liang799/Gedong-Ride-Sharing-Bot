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
        try:
            location = MapLocation(location_url)
        except Exception as e:
            exception_message = str(e)
            await update.message.reply_text(f"An error occurred: {exception_message}")
            return SELECTING_PASSENGER_DESTINATION

        kb = [[
            KeyboardButton("Click here to see list of potential drivers",
                           web_app=WebAppInfo(
                               f"https://example.com/passenger/@{location.lat_long.lat},{location.lat_long.long}"))
        ]]
        await update.message.reply_text(f"Received location: {location.location_name} "
                                        f"@{location.lat_long.lat},{location.lat_long.long}",
                                        reply_markup=ReplyKeyboardMarkup(kb))

        repository.addPassenger(
            PotentialPassenger(update.message.from_user.id, location)
        )
        return ConversationHandler.END

    return selecting_passenger_destination


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text('Bye! Hope to talk to you again soon.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
