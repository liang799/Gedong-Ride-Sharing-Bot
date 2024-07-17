import asyncio
import os

from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from bot_cmds.driver_cmds import drive_to

load_dotenv()

bot_api_token = os.getenv("BOT_API_TOKEN")

api_id = int(os.getenv("CLIENT_API_ID"))
api_hash = os.getenv("CLIENT_API_HASH")
session_str = os.getenv("CLIENT_SESSION")


async def testing():
    client = TelegramClient(
        StringSession(session_str), api_id, api_hash,
        sequential_updates=True
    )
    await client.connect()
    await client.get_me()
    await client.get_dialogs()

    print("connected!!!!")

    async with client.conversation("@gedong_ride_share_bot", timeout=5) as conv:
        print("Chat with bot!")
        await conv.send_message("/drive_to")
        print("sent!")
        resp = await conv.get_response()
        print('Response:')
        print(resp)


async def main() -> None:
    application = Application.builder().token(bot_api_token).build()
    application.add_handler(CommandHandler("drive_to", drive_to))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    await testing()

    await application.stop()


if __name__ == "__main__":
    asyncio.run(main())
