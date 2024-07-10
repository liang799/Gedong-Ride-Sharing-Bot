import pytest_asyncio
import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()

# Your API ID, hash and session string here
api_id = int(os.getenv("CLIENT_API_ID"))
api_hash = os.getenv("CLIENT_API_HASH")
session_str = os.getenv("CLIENT_SESSION")


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
