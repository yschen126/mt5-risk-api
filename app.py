from flask import Flask, request, jsonify
import MetaTrader5 as mt5
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return 'MT5 Risk API is running.'

@app.route('/check', methods=['POST'])
def check_mt5_status():
    data = request.get_json()
    login_id = int(data.get('login_id'))
    password = data.get('password')
    server = data.get('server')

    # 嘗試初始化 MT5
    if not mt5.initialize():
        return jsonify({"error": "MT5 初始化失敗", "details": mt5.last_error()}), 500

    # 登入 MT5
    authorized = mt5.login(login=login_id, password=password, server=server)
    if not authorized:
        mt5.shutdown()
        return jsonify({"error": "MT5 登入失敗", "details": mt5.last_error()}), 401

    # 取得帳戶資訊
    account_info = mt5.account_info()
    if account_info is None:
        mt5.shutdown()
        return jsonify({"error": "無法取得帳戶資訊", "details": mt5.last_error()}), 500

    # 組成回應資料
    result = {
        "login_id": login_id,
        "account_balance": account_info.balance,
        "equity": account_info.equity,
        "floating_loss": account_info.profit,
        "margin": account_info.margin,
        "margin_free": account_info.margin_free,
        "margin_level": account_info.margin_level,
        "server_time": datetime.now().isoformat(),
        "connection": "CONNECTED" if mt5.connection_status() == mt5.CONNECTION_CONNECTED else "DISCONNECTED"
    }

    mt5.shutdown()
    return jsonify(result)
