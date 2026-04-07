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
BOT_TOKEN = "8661537357:AAF050il-maWYpmu6yjG66M9QBUEF5uXVdQ"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Working 24/7 on Render!")

def run_bot():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

# 3. Start both simultaneously
if __name__ == "__main__":
    # Start the web server in a separate thread
    t = Thread(target=run_web_server)
    t.start()
    
    # Run the bot in the main thread
    run_bot()
