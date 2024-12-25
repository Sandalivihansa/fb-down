import re
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import yt_dlp

# Load environment variables
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# Create a Pyrogram client
app = Client("fb_video_downloader_bot",
             bot_token=TELEGRAM_TOKEN,
             api_id=API_ID,
             api_hash=API_HASH)

# Function to download Facebook video
def download_video(url: str):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.%(ext)s',
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info_dict)

# Start command handler
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 Creator", url="https://t.me/deweni2"),
         InlineKeyboardButton("💬 Support", url="https://t.me/slmusicmania")]
    ])
    await message.reply_photo(
        photo="https://telegra.ph/file/7927a81cd927d35fc8437.jpg",
        caption="**Hi! I'm your Facebook Video Downloader Bot. 🎥**\n\n"
                "Send me a Facebook video link, and I'll download it for you!",
        reply_markup=buttons
    )

# Message handler for downloading videos in private chat
@app.on_message(filters.text & filters.private)
async def handle_private_message(client, message):
    url = message.text.strip()

    # Regex to validate Facebook video URLs
    fb_url_pattern = r'(https?://(?:www\.)?facebook\.com/.+/videos/\d+|https?://fb\.watch/\S+)'

    if re.match(fb_url_pattern, url):
        await message.reply_text("Downloading the video... Please wait.⏳")
        try:
            # Download the video
            video_file = download_video(url)

            # Send the video back to the user
            await app.send_video(chat_id=message.chat.id, video=video_file)

            # Clean up after sending the video
            os.remove(video_file)
            await message.reply_text("Video downloaded successfully!✅")
        except Exception as e:
            await message.reply_text(f"An error occurred while downloading the video🚫: {e}")
    else:
        await message.reply_text("Please send a valid Facebook video link.😬")

# Message handler for downloading videos in groups
@app.on_message(filters.text & filters.group)
async def handle_group_message(client, message):
    url = message.text.strip()

    # Regex to validate Facebook video URLs
    fb_url_pattern = r'(https?://(?:www\.)?facebook\.com/.+/videos/\d+|https?://fb\.watch/\S+)'

    if re.match(fb_url_pattern, url):
        await message.reply_text("Downloading the video... Please wait.⏳")
        try:
            # Download the video
            video_file = download_video(url)

            # Send the video to the group
            await app.send_video(chat_id=message.chat.id, video=video_file)

            # Clean up after sending the video
            os.remove(video_file)
            await message.reply_text("Video downloaded successfully!✅")
        except Exception as e:
            await message.reply_text(f"An error occurred while downloading the video🚫: {e}")
    else:
        await message.reply_text("Please send a valid Facebook video link.😬")

# Start the bot
if __name__ == '__main__':
    app.run()
