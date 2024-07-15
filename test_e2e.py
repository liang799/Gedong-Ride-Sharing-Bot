import pytest
from telethon import TelegramClient

pytest_plugins = 'pytest_asyncio'


# @pytest.mark.asyncio(scope="session")  # The asyncio event loop must not change after connection
# async def test_help(client: TelegramClient):
#     message = await client.send_message("@gedong_ride_share_bot", "/help")
#     assert message.replies == ""

@pytest.mark.asyncio(scope="session")  # The asyncio event loop must not change after connection
async def test_no_match_because_passenger_drop_off_point_too_far(client: TelegramClient):
    driver = User()
    driver.send_driving_destination_to_bot()

    passenger = User()
    passenger.send_drop_off_point_to_bot()
    bot.should_show_waiting_ui_for_passenger()

    bot.decides_that_passenger_destination_is_too_far()
    bot.should_not_inform_driver_about_potential_passenger()
    bot.should_not_list_driver_in_passenger_waiting_screen()






