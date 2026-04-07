import os
from flask import Flask
from threading import Thread
import telebot

# 1. Setup Flask for Render
app = Flask('')

@app.route('/')
def home():
    return "I'm alive"
def run_web_server():
    # Render provides the PORT environment variable automatically
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# 2. Setup your Bot
BOT_TOKEN = "8592897208:AAEhFHK5LC2u_lTBmseas6tFv_LJd9cyCnY"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Working 24/7 on Render!")

def run_bot():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Using your actual Render URL to ensure the link works everywhere
    file_id = message.photo[-1].file_id
    link = f"https://demo-project-1ty6.onrender.com/view/{file_id}"
    bot.reply_to(message, f"Link generated for demonstration:\n{link}")
# 3. Start both simultaneously
if __name__ == '__main__':
    # 1. Start the Telegram Bot in a separate background thread
    bot_thread = Thread(target=lambda: bot.infinity_polling(timeout=10, long_polling_timeout=5))
    bot_thread.daemon = True  # Ensures the thread closes when the app stops
    bot_thread.start()
    
    # 2. Start the Flask Web Server (This stays in the foreground)
    # Render provides the 'PORT' environment variable automatically
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
