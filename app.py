from flask import Flask, request, jsonify, send_file
import pandas as pd
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = '/tmp/form_data.json'
EXCEL_FILE = '/tmp/form_responses.xlsx'
CONFIG_FILE = '/tmp/form_config.json'
ADMIN_PASSWORD = 'admin123'

# 預設表單配置
DEFAULT_CONFIG = {
    "title": "亞馬遜業務聯繫表單",
    "fields": [
        {"name": "question1", "label": "公司名稱", "type": "text", "required": True, "options": []},
        {"name": "question2", "label": "聯絡人姓名", "type": "text", "required": True, "options": []},
        {"name": "question3", "label": "聯絡電話(手機)", "type": "tel", "required": True, "options": []},
        {"name": "question4", "label": "Line ID (亞馬遜人員會協助聯繫您的業務經理與您建立Line群組)", "type": "text", "required": True, "options": []},
        {"name": "question5", "label": "請問您要使用的【註冊信箱】 填寫後亞馬遜人員會直接*發送連結*到您這個信箱並協助建立Line 群組後續溝通", "type": "email", "required": True, "options": []},
        {"name": "question6", "label": "請問對於開設哪一個亞馬遜站點有興趣?", "type": "select", "required": True, "options": ["美國站點 (Amazon.com)", "歐洲站點 (Amazon.co.uk, Amazon.de, Amazon.fr, Amazon.it, Amazon.es)", "日本站點 (Amazon.co.jp)", "加拿大站點 (Amazon.ca)", "澳洲站點 (Amazon.com.au)", "多個站點"]}
    ]
}

@app.route('/')
def index():
    return send_file('form.html')

@app.route('/admin-login', methods=['POST'])
def admin_login():
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        if password == ADMIN_PASSWORD:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': '密碼錯誤'})
    except Exception as e:
        return jsonify({'success': False, 'message': '登入失敗'})

@app.route('/get-config', methods=['GET'])
def get_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = DEFAULT_CONFIG
    return jsonify(config)

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        if not request.is_json:
            return jsonify({'status': 'error', 'message': '請求格式錯誤'}), 400
            
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': '沒有收到資料'}), 400
            
        records = []
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    records = json.load(f)
            except:
                records = []
        
        records.append(data)
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        
        return jsonify({'status': 'success', 'message': '資料已成功儲存'})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'服務器錯誤: {str(e)}'}), 500

# Vercel需要這個
app = app
