
from flask import Flask, send_file, request
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime
import os

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
        text = "00:00:00"
    else:
        days = delta.days
        hours, rem = divmod(delta.seconds, 3600)
        minutes = rem // 60
        text = f"{days:02}:{hours:02}:{minutes:02}"

    img = Image.new("RGB", (450, 150), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_main = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 50)
        font_label = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except:
        font_main = ImageFont.load_default()
        font_label = ImageFont.load_default()

    bbox = font_main.getbbox(text)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((450 - w) // 2, 30), text, font=font_main, fill=(255, 0, 0))  # crvena

    # Oznake ispod: Dana, Sati, Minuta
    labels = ["Dana", "Sati", "Minuta"]
    segment_width = 450 // 3
    for i, label in enumerate(labels):
        text_w = draw.textlength(label, font=font_label)
        x = segment_width * i + (segment_width - text_w) // 2
        draw.text((x, 100), label, font=font_label, fill=(0, 0, 0))

    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
