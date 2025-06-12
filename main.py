from flask import Flask, send_file, request, jsonify
from datetime import datetime
from PIL import Image
import io
import logging
import os
import hashlib
import random
import time

app = Flask(__name__)

# Ẩn log Flask mặc định
import logging as py_logging
py_logging.getLogger('werkzeug').setLevel(py_logging.ERROR)

# File log
log_file = 'track.log'
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Lấy IP thực
def get_client_ip():
    xff = request.headers.get('X-Forwarded-For', '')
    return xff.split(',')[0].strip() if xff else request.remote_addr

# Ghi log truy cập
def log_request():
    ip = get_client_ip()
    timestamp = datetime.utcnow().isoformat()
    user_agent = request.headers.get('User-Agent', 'Unknown')
    path = request.path
    query = request.query_string.decode()
    uid = request.args.get("uid", "")
    version = request.args.get("v", "")
    hash_id = hashlib.md5(os.urandom(16)).hexdigest()

    log_msg = (
        f"[TRACK] IP: {ip} | Time: {timestamp} | "
        f"Path: {path}?{query} | UID: {uid} | "
        f"Version: {version} | UA: {user_agent} | ID: {hash_id}"
    )
    logging.info(log_msg)

# Tạo ảnh GIF 1x1 trong suốt
def generate_tracking_gif():
    img = Image.new('RGBA', (1, 1), (255, 255, 255, 0))
    buffer = io.BytesIO()
    img.save(buffer, format='GIF')
    buffer.seek(0)
    return buffer

@app.route('/track.gif')
def track():
    log_request()
    buffer = generate_tracking_gif()
    return send_file(buffer, mimetype='image/gif')

@app.route('/log')
def view_log():
    try:
        with open(log_file, 'r') as f:
            content = f.read()
        return f"<pre style='white-space: pre-wrap;'>{content}</pre>"
    except FileNotFoundError:
        return 'Log file not found.', 404

# ✅ Route sinh URL tracking
@app.route('/gen')
def generate_tracking_url():
    base_url = request.url_root.rstrip('/') + '/track.gif'
    uid = request.args.get('uid', '')
    timestamp = int(time.time())
    rand_hash = hashlib.md5(str(random.random()).encode()).hexdigest()[:6]

    # Tạo link với query
    link = f"{base_url}?v={timestamp}_{rand_hash}"
    if uid:
        link += f"&uid={uid}"

    return f"""
    <h3>✅ Tracking Link:</h3>
    <code>{link}</code><br><br>
    <a href="{link}" target="_blank">Preview</a>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
