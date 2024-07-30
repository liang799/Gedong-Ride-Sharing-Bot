import asyncio

import pytest_asyncio
import os

from telegram.ext import ApplicationBuilder, Application, CommandHandler, ConversationHandler, MessageHandler, filters
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
import logging

from bot_cmds.driver_cmds import *
from bot_cmds.passenger_cmds import *

load_dotenv()

# Your API ID, hash and session string here
api_id = int(os.getenv("CLIENT_API_ID"))
api_hash = os.getenv("CLIENT_API_HASH")
session_str = os.getenv("CLIENT_SESSION")

bot_api_token = os.getenv("BOT_API_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


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
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("drive_to", drive_to), CommandHandler("drop_off", drop_off)],
        states={
            SELECTING_DRIVER_DESTINATION: [MessageHandler(filters.TEXT, selecting_driver_destination)],
            SELECTING_PASSENGER_DESTINATION: [MessageHandler(filters.TEXT, selecting_passenger_destination)]
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
