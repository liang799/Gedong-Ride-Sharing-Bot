import pytest
from telegram.ext import Application
from telethon import TelegramClient

from LatLong import LatLong

pytest_plugins = 'pytest_asyncio'


class TelegramBot:
    def __init__(self, bot: Application):
        self.passenger_lat_long = None
        self.driver_lat_long = None
        self.bot = bot

    def decides_that_passenger_destination_is_too_far(self):
        dist_km = self.driver_lat_long.compare_distance_km(self.passenger_lat_long)
        assert dist_km > 5.0

    def saveDriver(self, lat_long: LatLong):
        self.driver_lat_long = lat_long

    def savePassenger(self, lat_long: LatLong):
        self.passenger_lat_long = lat_long

    def should_notify_driver_of_potential_passenger(self):
        pass


class User:
    def __init__(self, client: TelegramClient):
        self.client = client

    async def send_driving_destination_to(self, bot: TelegramBot):
        async with self.client.conversation("@gedong_ride_share_bot", timeout=5) as conv:
            await conv.send_message("/drive_to")
            resp = await conv.get_response()
            assert resp.text in "Please share the Google Map URL Location. Example: " \
                                "https://maps.app.goo.gl/UuEC3fpGAHV9a7K38"
            await conv.send_message("https://maps.app.goo.gl/Tx15MVpNw6xuPuz77")
            resp = await conv.get_response()
            assert resp.text in "Received location: Hougang Mall " \
                                "@1.372455,103.8938277"
            bot.saveDriver(LatLong(1.372455, 103.8938277))

    async def send_far_drop_off_point_to(self, bot: TelegramBot):
        async with self.client.conversation("@gedong_ride_share_bot", timeout=5) as conv:
            await conv.send_message("/drop_off")
            resp = await conv.get_response()
            assert resp.text in "Please share the Google Map URL Location. Example: " \
                                "https://maps.app.goo.gl/UuEC3fpGAHV9a7K38"
            await conv.send_message("https://maps.app.goo.gl/Rd7ocD8Ao6FHbL597")
            resp = await conv.get_response()
            assert resp.text in "Received location: West Coast Park " \
                                "@1.3140476,103.7416346"
            bot.savePassenger(LatLong(1.3140476, 103.7416346))

    async def send_near_drop_off_point_to(self, bot):
        async with self.client.conversation("@gedong_ride_share_bot", timeout=5) as conv:
            await conv.send_message("/drop_off")
            resp = await conv.get_response()
            assert resp.text in "Please share the Google Map URL Location. Example: " \
                                "https://maps.app.goo.gl/UuEC3fpGAHV9a7K38"
            await conv.send_message("https://maps.app.goo.gl/Tx15MVpNw6xuPuz77")
            resp = await conv.get_response()
            assert resp.text in "Received location: Hougang Mall " \
                                "@1.372455,103.8938277"
            bot.saveDriver(LatLong(1.372455, 103.8938277))


@pytest.mark.asyncio(scope="session")  # The asyncio event loop must not change after connection
async def test_no_match_because_passenger_drop_off_point_too_far(client: TelegramClient, bot_api: Application):
    bot = TelegramBot(bot_api)
    driver = User(client)
    await driver.send_driving_destination_to(bot)

    passenger = User(client)
    await passenger.send_far_drop_off_point_to(bot)

    bot.decides_that_passenger_destination_is_too_far()


@pytest.mark.asyncio(scope="session")  # The asyncio event loop must not change after connection
async def test_notifying_driver_of_potential_passenger(client: TelegramClient, bot_api: Application):
    bot = TelegramBot(bot_api)

    passenger = User(client)
    await passenger.send_near_drop_off_point_to(bot)

    driver = User(client)
    await driver.send_driving_destination_to(bot)   # todo: create a separate function that has assertion in it
