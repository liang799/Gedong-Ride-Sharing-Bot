import pytest
from geopy import distance
from telegram.ext import Application
from telethon import TelegramClient

pytest_plugins = 'pytest_asyncio'


class LatLong:
    def __init__(self, lat: float, long: float):
        self.lat = lat
        self.long = long

    def compare_distance_km(self, other_lat_long: 'LatLong'):
        coords_1 = (self.lat, self.long)
        coords_2 = (other_lat_long.lat, other_lat_long.long)
        return distance.geodesic(coords_1, coords_2).km


class TelegramBot:
    state = 'idle'

    def __init__(self, bot: Application):
        self.passenger_lat_long = None
        self.driver_lat_long = None
        self.bot = bot

    def decides_that_passenger_destination_is_too_far(self):
        if self.driver_lat_long.compare_distance_km(self.passenger_lat_long) > 5:
            assert self.state == 'idle'
            return

    def should_not_inform_driver_about_potential_passenger(self):
        assert self.state == 'idle'

    def should_not_list_driver_in_passenger_waiting_screen(self):
        assert self.state == 'idle'

    def saveDriver(self, lat_long: LatLong):
        self.driver_lat_long = lat_long

    def savePassenger(self, lat_long: LatLong):
        self.passenger_lat_long = lat_long

    def setBotState(self, state: str):
        self.state = state


class User:
    def __init__(self, client: TelegramClient):
        self.client = client

    async def send_driving_destination_to(self, bot: TelegramBot):
        async with self.client.conversation("@gedong_ride_share_bot", timeout=5) as conv:
            await conv.send_message("/drive_to")
            bot.setBotState("busy")
            resp = await conv.get_response()
            assert resp.text in "Please share the Google Map URL Location. Example: " \
                                "https://maps.app.goo.gl/UuEC3fpGAHV9a7K38"
            await conv.send_message("https://maps.app.goo.gl/Tx15MVpNw6xuPuz77")
            resp = await conv.get_response()
            assert resp.text in "Received location: Hougang Mall " \
                                "@1.372455,103.8938277"
            bot.saveDriver(LatLong(1.372455, 103.8938277))
            bot.setBotState("idle")

    async def send_drop_off_point_to(self, bot: TelegramBot):
        async with self.client.conversation("@gedong_ride_share_bot", timeout=5) as conv:
            await conv.send_message("/drop_off")
            bot.setBotState("busy")
            resp = await conv.get_response()
            assert resp.text in "Please share the Google Map URL Location. Example: " \
                                "https://maps.app.goo.gl/UuEC3fpGAHV9a7K38"
            await conv.send_message("https://maps.app.goo.gl/Rd7ocD8Ao6FHbL597")
            resp = await conv.get_response()
            assert resp.text in "Received location: West Coast Park " \
                                "@1.3140476,103.7416346"
            bot.savePassenger(LatLong(1.372455, 103.8938277))
            bot.setBotState("idle")


@pytest.mark.asyncio(scope="session")  # The asyncio event loop must not change after connection
async def test_no_match_because_passenger_drop_off_point_too_far(client: TelegramClient, bot_api: Application):
    bot = TelegramBot(bot_api)
    driver = User(client)
    await driver.send_driving_destination_to(bot)

    passenger = User(client)
    await passenger.send_drop_off_point_to(bot)

    bot.decides_that_passenger_destination_is_too_far()
    bot.should_not_inform_driver_about_potential_passenger()
