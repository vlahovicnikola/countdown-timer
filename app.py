
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

    img = Image.new("RGBA", (450, 150), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    try:
        font_main = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 50)
        font_label = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except:
        font_main = ImageFont.load_default()
        font_label = ImageFont.load_default()

    if delta.total_seconds() <= 0:
        message = "PONUDA JE ISTEKLA!"
        try:
            font_main = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        except:
            font_main = ImageFont.load_default()
        bbox = font_main.getbbox(message)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (450 - text_width) // 2
        text_y = (150 - text_height) // 2
        draw.text((text_x, text_y), message, font=font_main, fill=(255, 0, 0, 255))
    else:
        days = delta.days
        hours, rem = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        values = [f"{days:02}", f"{hours:02}", f"{minutes:02}", f"{seconds:02}"]
        labels = ["Dana", "Sati", "Minuta", "Sekundi"]
        segment_width = 450 // 4

        for i in range(4):
            value = values[i]
            label = labels[i]
            v_bbox = font_main.getbbox(value)
            v_width = v_bbox[2] - v_bbox[0]
            v_x = segment_width * i + (segment_width - v_width) // 2
            draw.text((v_x, 30), value, font=font_main, fill=(255, 0, 0, 255))
            l_width = draw.textlength(label, font=font_label)
            l_x = segment_width * i + (segment_width - l_width) // 2
            draw.text((l_x, 95), label, font=font_label, fill=(0, 0, 0, 255))

    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
