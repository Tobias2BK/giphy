from flask import *
from datetime import datetime

app = Flask(__name__)

@app.route('/test.gif')
def track():
    ip = request.headers.get('X-Forwarded-For',request.remote_addr)
    time = datetime.utcnow().isoformat()
    print(f'Time: {time} - Ip: {ip}')
    return send_file('test.gif',mimetype='image/gif')
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
