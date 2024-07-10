import pytest
from telethon import TelegramClient

pytest_plugins = 'pytest_asyncio'


@pytest.mark.asyncio(scope="session")  # The asyncio event loop must not change after connection
async def test_help(client: TelegramClient):
    message = await client.send_message("@gedong_ride_share_bot", "/help")
    assert message.replies == ""
