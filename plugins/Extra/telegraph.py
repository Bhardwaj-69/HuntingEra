# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegraph import upload_file
from utils import get_file_id

@Client.on_message(filters.command("telegraph") & filters.private)
async def telegraph_upload(bot, update):
    t_msg = await bot.ask(
        chat_id=update.from_user.id, 
        text="📤 Send me a **photo or video** (under **5MB**) to get a Telegraph link."
    )

    file_info = get_file_id(t_msg)
    if not file_info:
        return await update.reply_text("❌ **Not supported!** Please send an image or video.")

    text = await update.reply_text(
        text="⏳ **Downloading...**", 
        disable_web_page_preview=True
    )   
    
    # Download the media file
    media = await t_msg.download()

    if not media:
        return await text.edit_text("❌ **Failed to download the file.**")

    await text.edit_text(
        text="📤 **Uploading to Telegraph...**", 
        disable_web_page_preview=True
    )                                            

    try:
        response = upload_file(media)  # Returns a list, not a dict

        if isinstance(response, list) and response:
            telegraph_url = f"https://graph.org{response[0]}"
        else:
            return await text.edit_text("❌ **Telegraph upload failed.**")

    except Exception as error:
        return await text.edit_text(f"❌ **Error:** `{error}`")

    finally:
        # Clean up the file after upload
        os.remove(media)

    # Send the response with buttons
    await text.edit_text(
        text=f"✅ **Telegraph Link:**\n\n<code>{telegraph_url}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔗 Open Link", url=telegraph_url),
                InlineKeyboardButton("📤 Share Link", url=f"https://telegram.me/share/url?url={telegraph_url}")
            ],
            [
                InlineKeyboardButton("✗ Close ✗", callback_data="close")
            ]
        ])
    )
