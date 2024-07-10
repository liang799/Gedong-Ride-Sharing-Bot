import asyncio
import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

load_dotenv()


async def main():
    async with TelegramClient(StringSession(os.getenv("CLIENT_SESSION")), os.getenv("CLIENT_API_ID"),
                              os.getenv("CLIENT_API_HASH")) as client:
        print("Your session string is:", client.session.save())
        # me = await client.get_me()
        # print(me.stringify())
        await client.connect()
        # Issue a high level command to start receiving message
        await client.get_me()
        # Fill the entity cache
        await client.get_dialogs()


# Create and run the event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
