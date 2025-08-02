from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/')
def home():
    return 'MT5 Risk API is running.'

@app.route('/check', methods=['POST'])
def check_risk():
    data = request.get_json()
    login_id = data.get('login_id')
    password = data.get('password')
    server = data.get('server')

    print(f"Received: {login_id}, {password}, {server}")
    time.sleep(1)

    return jsonify({
        "risk_level": "Medium",
        "floating_loss": -126.54,
        "margin_usage": "34.2%",
        "account_balance": 3124.88
    })