from flask import Flask, send_file, request
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime
import os  # ⬅️ važno za Render

app = Flask(__name__)

@app.route('/timer')
def timer():
    end = request.args.get("end")
    try:
        end_time = datetime.fromisoformat(end)
    except:
        return "Invalid datetime. Use format: YYYY-MM-DDTHH:MM:SS", 400

    now = datetime.utcnow()
    delta = end_time - now
    if delta.total_seconds() <= 0:
        text = "00:00:00:00"
    else:
        days = delta.days
        hours, rem = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        text = f"{days:02}:{hours:02}:{minutes:02}:{seconds:02}"

    img = Image.new("RGB", (450, 120), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 50)
    except:
        font = ImageFont.load_default()

    bbox = font.getbbox(text)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((450 - w) // 2, (120 - h) // 2), text, font=font, fill=(0, 0, 0))

    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

# ✅ Port za lokalno i Render okruženje
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # koristi PORT iz Render okruženja
    app.run(host='0.0.0.0', port=port)
