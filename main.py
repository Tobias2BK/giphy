from flask import *
from datetime import datetime
import logging
import os

app = Flask(__name__)

# Cấu hình ghi log vào file
log_file = 'track.log'
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

@app.route('/log')
def view_log():
    try:
        with open('track.log', 'r') as f:
            content = f.read()
        # Hiển thị log dưới dạng văn bản trong trình duyệt
        return f"<pre>{content}</pre>"
    except FileNotFoundError:
        return 'Log file not found.', 404


@app.route('/test.gif')
def track():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    time = datetime.utcnow().isoformat()
    logging.info(f'Time: {time} - IP: {ip}')
    gif_path = 'test.gif'
    if not os.path.exists(gif_path):
        return 'GIF not found', 404
    return send_file(gif_path, mimetype='image/gif')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
