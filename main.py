from flask import Flask, send_file, request, abort
from datetime import datetime
from PIL import Image, GifImagePlugin
import io
import logging
import random
import os
import hashlib

app = Flask(__name__)

# Cấu hình ghi log
log_file = 'track.log'
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - IP: %(message)s'
)

@app.route('/log')
def view_log():
    try:
        with open(log_file, 'r') as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except FileNotFoundError:
        return 'Log file not found.', 404

@app.route('/track.gif')
def track():
    # Lấy IP client
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    timestamp = datetime.utcnow().isoformat()
    logging.info(f'{ip} - {timestamp}')

    # Load ảnh gốc
    original = Image.open('test.gif')

    # Lấy frame đầu (nếu ảnh động)
    frame = original.copy().convert('RGB')
    pixels = frame.load()

    # Thêm nhiễu nhẹ
    for _ in range(10):
        x = random.randint(0, frame.width - 1)
        y = random.randint(0, frame.height - 1)
        r, g, b = pixels[x, y]
        pixels[x, y] = (
            (r + random.randint(-1, 1)) % 256,
            (g + random.randint(-1, 1)) % 256,
            (b + random.randint(-1, 1)) % 256,
        )

    # Tạm lưu vào buffer dưới dạng GIF (giữ định dạng gốc)
    buffer = io.BytesIO()
    frame.save(
        buffer,
        format='GIF',
        save_all=True,
        append_images=[original.copy()],
        loop=0,
        comment=f"Tracked at {timestamp}, hash={hashlib.md5(os.urandom(16)).hexdigest()}".encode('utf-8')
    )
    buffer.seek(0)

    # Gửi về client
    return send_file(buffer, mimetype='image/gif')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
