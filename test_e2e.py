import pytest
from telegram.ext import Application
from telethon import TelegramClient

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

    async def send_drop_off_point_to_bot(self):
        async with self.client.conversation("@gedong_ride_share_bot", timeout=5) as conv:
            await conv.send_message("/drop_off")
            resp = await conv.get_response()
            assert resp.text in "Please share the Google Map URL Location. Example: " \
                                "https://maps.app.goo.gl/UuEC3fpGAHV9a7K38"
            await conv.send_message("https://maps.app.goo.gl/Rd7ocD8Ao6FHbL597")
            resp = await conv.get_response()
            assert resp.text in "Received location: West Coast Park " \
                                "@1.3140476,103.7416346"


class TelegramBot:
    def __init__(self, bot: Application):
        self.bot = bot
        pass

    def should_show_waiting_ui_for_passenger(self):
        pass

    def decides_that_passenger_destination_is_too_far(self):
        pass

    def should_not_inform_driver_about_potential_passenger(self):
        pass

    def should_not_list_driver_in_passenger_waiting_screen(self):
        pass


@pytest.mark.asyncio(scope="session")  # The asyncio event loop must not change after connection
async def test_no_match_because_passenger_drop_off_point_too_far(client: TelegramClient, bot_api: Application):
    bot = TelegramBot(bot_api)
    driver = User(client)
    await driver.send_driving_destination_to_bot()

    passenger = User(client)
    await passenger.send_drop_off_point_to_bot()
    bot.should_show_waiting_ui_for_passenger()

    bot.decides_that_passenger_destination_is_too_far()
    bot.should_not_inform_driver_about_potential_passenger()
    bot.should_not_list_driver_in_passenger_waiting_screen()
