from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # 允许所有来源的跨域请求

# 新增的日志文件读取 API
@app.route('/api/read-log', methods=['GET'])
def read_log():
    log_path = request.args.get('path')
    if os.path.exists(log_path):
        with open(log_path, 'r') as file:
            logs = file.read()
        return jsonify({"logs": logs})
    else:
        return jsonify({"error": "File not found"}), 404

# 根路径
@app.route('/')
def index():
    return "OpenAI Log Analysis API"

# 用户信息
users = {
    "admin": "password"
}

# 用户登录 API
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username in users and users[username] == password:
        return jsonify({"token": "dummy-token"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

# 日志预测 API
@app.route('/api/predict/auth', methods=['POST'])
def predict_auth_logs():
    data = request.json
    logs = data.get('logs', [])
    predictions = []
    for log in logs:
        predictions.append({"log_message": log, "prediction": "anomaly" if "error" in log else "normal"})

    return jsonify(predictions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
