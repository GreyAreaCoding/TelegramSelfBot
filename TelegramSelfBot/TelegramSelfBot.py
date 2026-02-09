import os
import asyncio
from telethon import TelegramClient
from telethon.errors import FloodWaitError

# ────────────────────────────────────────────────
#               FILL THESE IN
# ────────────────────────────────────────────────
API_ID = 00000  # ← your api id
API_HASH = "1234978965sqdfqsdf"  # ← your api hash
PHONE = "+1234879"  # your phone number
CHANNEL = "@ChanelName"  # or -100123456789 (chat ID)
MEDIA_FOLDER = "images"
POST_INTERVAL = 300  # seconds (3600 = 1 hour)
# ────────────────────────────────────────────────
client = TelegramClient("session_name", API_ID, API_HASH)


async def send_album():
    file_paths = []
    for filename in os.listdir(MEDIA_FOLDER):
        full_path = os.path.join(MEDIA_FOLDER, filename)
        if os.path.isfile(full_path):
            lower = filename.lower()
            if lower.endswith(
                (".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mov", ".mkv")
            ):
                file_paths.append(full_path)

    if not file_paths:
        print("No supported media files found.")
        return False

    print(f"Found {len(file_paths)} files → sending as one album...")

    try:
        await client.send_file(
            entity=CHANNEL,
            file=file_paths,
            caption="""This is an album of media files sent by a self-bot.
You can customize the caption as needed. Each file in the album will be sent together in one message, and Telegram will display them as an album in the chat.
""",
            silent=True,
        )
        print(f"Album sent successfully ({len(file_paths)} items in one message)")

        return True

    except FloodWaitError as e:
        print(f"Flood wait → sleeping {e.seconds} seconds")
        await asyncio.sleep(e.seconds)
        return False
    except Exception as e:
        print(f"Error sending album: {type(e).__name__} → {e}")
        return False


async def main():
    await client.start(phone=PHONE)
    print("Logged in successfully")

    try:
        entity = await client.get_entity(CHANNEL)
        print(
            f"Target: {entity.title if hasattr(entity, 'title') else entity.username}"
        )
    except Exception as e:
        print(f"Cannot access channel: {e}")
        return

    while True:
        success = await send_album()

        if not success:
            print("Nothing sent or error → retry in 5 min")
            await asyncio.sleep(300)
        else:
            print("Waiting 5 minutes before next folder check...")
            await asyncio.sleep(300)


if __name__ == "__main__":
    asyncio.run(main())
