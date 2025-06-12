from flask import Flask, send_file, request, abort
from datetime import datetime
from PIL import Image, ImageSequence
import io
import logging
import random
import os
import hashlib

app = Flask(__name__)

# 🧹 Ẩn log mặc định của werkzeug
import logging as py_logging
py_logging.getLogger('werkzeug').setLevel(py_logging.ERROR)

# 📝 Cấu hình log riêng
log_file = 'track.log'
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# 📦 Hàm lấy IP thực
def get_client_ip():
    xff = request.headers.get('X-Forwarded-For', '')
    if xff:
        return xff.split(',')[0].strip()
    return request.remote_addr

# 🎯 Ghi log chi tiết
def log_request():
    ip = get_client_ip()
    timestamp = datetime.utcnow().isoformat()
    user_agent = request.headers.get('User-Agent', 'Unknown')
    path = request.path
    query = request.query_string.decode()
    hash_id = hashlib.md5(os.urandom(16)).hexdigest()
    logging.info(f'[TRACK] IP: {ip} | Time: {timestamp} | Path: {path}?{query} | UA: {user_agent} | ID: {hash_id}')

# 🖼️ Trả về ảnh GIF 1x1 để ẩn trong HTML
def generate_tracking_gif():
    img = Image.new('RGBA', (1, 1), (255, 255, 255, 0))  # Transparent
    buffer = io.BytesIO()
    img.save(buffer, format='GIF')
    buffer.seek(0)
    return buffer

@app.route('/track.gif')
def track():
    log_request()
    buffer = generate_tracking_gif()
    return send_file(buffer, mimetype='image/gif')

# 📄 Hiển thị log dưới dạng HTML
@app.route('/log')
def view_log():
    try:
        with open(log_file, 'r') as f:
            content = f.read()
        return f"<pre style='white-space: pre-wrap;'>{content}</pre>"
    except FileNotFoundError:
        return 'Log file not found.', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
