from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import json
import random
import string
import os
import sys
import asyncio
from datetime import datetime, timedelta
import pytz
import signal
import pyshorteners
import logging
import threading
import http.server
import socketserver

# ✅ Configuration
TOKEN = "7722342816:AAEkrArt2FHmKCcKap32AyKgnRootmzlV3M"
TIMEZONE = pytz.timezone('Asia/Kolkata')
PID_FILE = "bot.pid"

# ✅ Load channels from output.kkj file
def load_channels():
    channels = {}
    file_path = os.path.join(os.getcwd(), "output.kkj")  # Ensure correct path

    if not os.path.exists(file_path):
        print("❌ Error: Channel data file 'output.kkj' not found.")
        return channels

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if " = " in line:  # Ensure valid format
                    parts = line.split(" = ", 1)
                    name = parts[0].lstrip("0123456789. ").strip()
                    link = parts[1].strip()
                    channels[name.lower()] = {"name": name, "link": link}
    except Exception as e:
        print(f"❌ Error reading 'output.kkj': {e}")

    print(f"✅ Loaded {len(channels)} channels from 'output.kkj'")
    return channels


# ✅ Shorten URLs
def shorten_url(long_url):
    try:
        shortener = pyshorteners.Shortener()
        return shortener.tinyurl.short(long_url)
    except Exception as e:
        print(f"Error shortening URL: {e}")
        return long_url

# ✅ Delete messages after 15 minutes
async def delete_after_delay(messages, selection_message=None):
    await asyncio.sleep(480)
    for msg in messages:
        try:
            await msg.edit_text("Deleted for avoiding copyright. Tap /start to restart.")
        except:
            pass
    if selection_message:
        try:
            await selection_message.edit_text("Deleted. Tap /start to restart.", reply_markup=None)
        except:
            pass


# ✅ Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pdf_path = os.path.join(os.getcwd(), "cleaned_data_columns (2).pdf")

    # Send a message first
    await update.message.reply_text('''
📜 We currently have these channels available.Please check the attached list , 
find your favorate channel type name here  ,
you  will get a link , to play you need vlc player , 
copy link go to vlc player then on bottom 
there will be a button named as more tap there at there a button or place written with 
new sream click there paste link and just wait few seconds nd boom , enjoy ''')

    # Send the PDF file
    with open(pdf_path, "rb") as pdf_file:
        await update.message.reply_document(document=pdf_file, filename="Channel_List.pdf")

# ✅ Search Function
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.lower()
    channels = load_channels()

    if not channels:
        await update.message.reply_text("Error: Channel list is empty.")
        return

    matches = [channels[name] for name in channels if query in name]

    if not matches:
        await update.message.reply_text("No channels found. Try another keyword.")
        return

    buttons = [[InlineKeyboardButton(ch["name"], callback_data=ch["name"])] for ch in sorted(matches, key=lambda x: x["name"])[:20]]
    reply_markup = InlineKeyboardMarkup(buttons)

    selection_msg = await update.message.reply_text("Select channel:", reply_markup=reply_markup)
    asyncio.create_task(delete_after_delay([], selection_message=selection_msg))

# ✅ Handle Button Clicks
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    channel_name = query.data
    channels = load_channels()
    now = datetime.now(TIMEZONE)

    if channel_name.lower() not in channels:
        await query.message.reply_text("Channel not found.")
        return

    channel = channels[channel_name.lower()]

    # ✅ Check if link already exists in memory
    if channel_name in url_data:
        try:
            expiry = datetime.strptime(url_data[channel_name]["expiry"], "%Y-%m-%d %H:%M:%S")
            expiry = TIMEZONE.localize(expiry)
            if expiry > now and not url_data[channel_name]["link"].startswith("DELETED"):
                msg1 = await query.message.reply_text(f"Channel link for {channel_name}:")
                msg2 = await query.message.reply_text(url_data[channel_name]["link"])
                asyncio.create_task(delete_after_delay([msg1, msg2], selection_message=query.message))
                return
        except:
            pass

    # ✅ Generate new short URL
    short_link = shorten_url(channel["link"])

    url_data[channel_name] = {
        "link": short_link,
        "expiry": (now + timedelta(hours=17)).strftime("%Y-%m-%d %H:%M:%S")
    }

    msg1 = await query.message.reply_text(f"Channel link for {channel_name}:")
    msg2 = await query.message.reply_text(short_link)
    asyncio.create_task(delete_after_delay([msg1, msg2], selection_message=query.message))

# ✅ Auto-Refresh Expired Codes
async def refresh_codes(context: ContextTypes.DEFAULT_TYPE):
    try:
        now = datetime.now(TIMEZONE)

        for channel in url_data:
            try:
                expiry = datetime.strptime(url_data[channel]["expiry"], "%Y-%m-%d %H:%M:%S")
                expiry = TIMEZONE.localize(expiry)
                if now > expiry or now > expiry + timedelta(days=30):
                    url_data[channel]["link"] = "DELETED_" + shorten_url("https://expired-url.com")
                    url_data[channel]["expiry"] = now.strftime("%Y-%m-%d %H:%M:%S")
            except:
                url_data[channel]["link"] = "DELETED_" + shorten_url("https://expired-url.com")
                url_data[channel]["expiry"] = now.strftime("%Y-%m-%d %H:%M:%S")

        print("Codes refreshed")
    except Exception as e:
        print(f"Error refreshing codes: {e}")

# ✅ Run Bot
def main():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, 'r') as f:
                old_pid = int(f.read().strip())
            os.kill(old_pid, signal.SIGTERM)
            print(f"Terminated existing bot instance (PID: {old_pid})")
        except:
            pass
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))

    print("Initializing bot...")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
    app.add_handler(CallbackQueryHandler(button))

    app.job_queue.run_repeating(refresh_codes, interval=17*60*60, first=17*60*60)
    
    print("Starting bot...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

# Dummy Web Server to Prevent Koyeb Health Check Failure
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def run_dummy_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving HTTP on port {PORT} (Koyeb requirement)")
        httpd.serve_forever()

# Start Dummy Web Server in a Separate Thread
threading.Thread(target=run_dummy_server, daemon=True).start()

# Start the Telegram Bot
if __name__ == "__main__":
    main()
if __name__ == "__main__":
    try:
        signal.signal(signal.SIGINT, lambda s, f: (os.remove(PID_FILE), sys.exit(0)))
        signal.signal(signal.SIGTERM, lambda s, f: (os.remove(PID_FILE), sys.exit(0)))
        main()
    except KeyboardInterrupt:
        print("\nStopping bot...")
        os.remove(PID_FILE)
    except Exception as e:
        print(f"Fatal error: {e}")
        os.remove(PID_FILE)
        sys.exit(1)
