import pytest
from telegram.ext import Application
from telethon import TelegramClient

from LatLong import LatLong

pytest_plugins = 'pytest_asyncio'


class User:
    def __init__(self, client: TelegramClient):
        self.client = client

    async def send_driving_destination_to_bot(self):
        async with self.client.conversation("@gedong_ride_share_bot", timeout=5) as conv:
            await conv.send_message("/drive_to")
            resp = await conv.get_response()
            assert resp.text in "Please share the Google Map URL Location. Example: " \
                                "https://maps.app.goo.gl/UuEC3fpGAHV9a7K38"
            await conv.send_message("https://maps.app.goo.gl/Tx15MVpNw6xuPuz77")
            resp = await conv.get_response()
            assert resp.text in "Received location: Hougang Mall " \
                                "@1.372455,103.8938277"

    async def send_far_drop_off_point_to_bot(self):
        async with self.client.conversation("@gedong_ride_share_bot", timeout=5) as conv:
            await conv.send_message("/drop_off")
            resp = await conv.get_response()
            assert resp.text in "Please share the Google Map URL Location. Example: " \
                                "https://maps.app.goo.gl/UuEC3fpGAHV9a7K38"
            await conv.send_message("https://maps.app.goo.gl/Rd7ocD8Ao6FHbL597")
            resp = await conv.get_response()
            assert resp.text in "Received location: West Coast Park " \
                                "@1.3140476,103.7416346"

    async def send_near_drop_off_point_to_bot(self):
        async with self.client.conversation("@gedong_ride_share_bot", timeout=5) as conv:
            await conv.send_message("/drop_off")
            resp = await conv.get_response()
            assert resp.text in "Please share the Google Map URL Location. Example: " \
                                "https://maps.app.goo.gl/UuEC3fpGAHV9a7K38"
            await conv.send_message("https://maps.app.goo.gl/Tx15MVpNw6xuPuz77")
            resp = await conv.get_response()
            assert resp.text in "Received location: Hougang Mall " \
                                "@1.372455,103.8938277"


@pytest.mark.asyncio(scope="session")  # The asyncio event loop must not change after connection
async def test_no_match_because_passenger_drop_off_point_too_far(client: TelegramClient, bot_api: Application):
    driver = User(client)
    await driver.send_driving_destination_to_bot()

    passenger = User(client)
    await passenger.send_far_drop_off_point_to_bot()


@pytest.mark.asyncio(scope="session")  # The asyncio event loop must not change after connection
async def test_notifying_driver_of_potential_passenger(client: TelegramClient, bot_api: Application):
    passenger = User(client)
    await passenger.send_near_drop_off_point_to_bot()

    driver = User(client)
    await driver.send_driving_destination_to_bot()  # todo: create a separate function that has assertion in it
