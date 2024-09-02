from typing import List

import pytest_asyncio
import os

from telegram.ext import ApplicationBuilder, Application, CommandHandler, ConversationHandler, MessageHandler, filters
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
import logging

from bot_cmds.driver_cmds import *
from bot_cmds.passenger_cmds import *
from db.potentialpassenger import PotentialPassengerRepository, PotentialPassenger

load_dotenv()

# Your API ID, hash and session string here
api_id = int(os.getenv("CLIENT_API_ID"))
api_hash = os.getenv("CLIENT_API_HASH")
session_str = os.getenv("CLIENT_SESSION")

bot_api_token = os.getenv("BOT_API_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class LocalPassengerRepo(PotentialPassengerRepository):
    def __init__(self):
        self.passengers: List[PotentialPassenger] = []

    def getListOfPassengersWithin(self, lat_long: LatLong) -> List[PotentialPassenger]:
        return list(filter(
            lambda passenger: passenger.location.lat_long.compare_distance_km(lat_long) < 5,
            self.passengers
        ))

    def addPassenger(self, passenger: PotentialPassenger):
        self.passengers.append(passenger)


@pytest_asyncio.fixture(scope="session")
async def client() -> TelegramClient:
    client = TelegramClient(
        StringSession(session_str), api_id, api_hash,
        sequential_updates=True
    )
    # Setup
    await client.connect()
    await client.get_me()
    await client.get_dialogs()

    yield client

    # Teardown
    await client.disconnect()
    await client.disconnected


@pytest_asyncio.fixture(scope="session")
async def bot_api() -> Application:
    app = ApplicationBuilder().token(bot_api_token).build()
    passRepo = LocalPassengerRepo()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("drive_to", drive_to), CommandHandler("drop_off", drop_off)],
        states={
            SELECTING_DRIVER_DESTINATION: [MessageHandler(filters.TEXT, create_selecting_driver_destination(passRepo))],
            SELECTING_PASSENGER_DESTINATION: [MessageHandler(filters.TEXT, create_selecting_passenger_destination(passRepo))]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    app.add_handler(conv_handler)

    # Setup
    await app.initialize()
    await app.updater.start_polling()
    await app.start()

    yield app

    # Teardown
    await app.updater.stop()
    await app.stop()
    await app.shutdown()
