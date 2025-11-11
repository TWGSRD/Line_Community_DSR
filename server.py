from flask import Flask, request, jsonify, send_file
import pandas as pd
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'form_data.json'
EXCEL_FILE = 'form_responses.xlsx'
CONFIG_FILE = 'form_config.json'
ADMIN_PASSWORD = 'admin123'  # 管理者密碼，可自行修改

# 預設表單配置
DEFAULT_CONFIG = {
    "title": "群組資料填寫表單",
    "fields": [
        {"name": "question1", "label": "問題1", "type": "text", "required": True, "options": []},
        {"name": "question2", "label": "問題2", "type": "text", "required": True, "options": []},
        {"name": "question3", "label": "問題3", "type": "text", "required": True, "options": []},
        {"name": "question4", "label": "問題4", "type": "text", "required": True, "options": []},
        {"name": "question5", "label": "問題5", "type": "text", "required": True, "options": []},
        {"name": "question6", "label": "問題6", "type": "text", "required": True, "options": []}
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

@app.route('/save-config', methods=['POST'])
def save_config():
    try:
        config = request.get_json()
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/get-data', methods=['GET'])
def get_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                records = json.load(f)
            return jsonify(records)
        else:
            return jsonify([])
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # 確保接收JSON資料
        if not request.is_json:
            return jsonify({'status': 'error', 'message': '請求格式錯誤'}), 400
            
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': '沒有收到資料'}), 400
            
        print(f"收到提交資料: {data}")
        
        # 讀取現有資料
        records = []
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    records = json.load(f)
            except:
                records = []
        
        # 添加新資料
        records.append(data)
        
        # 儲存JSON檔案
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        
        # 儲存Excel檔案
        try:
            df = pd.DataFrame(records)
            df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
        except Exception as excel_error:
            print(f"Excel儲存錯誤: {excel_error}")
        
        print(f"資料已儲存，總記錄數: {len(records)}")
        return jsonify({'status': 'success', 'message': '資料已成功儲存'})
        
    except Exception as e:
        print(f"提交錯誤: {e}")
        return jsonify({'status': 'error', 'message': f'服務器錯誤: {str(e)}'}), 500

@app.route('/save-data', methods=['POST'])
def save_data():
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_json = f'form_data_backup_{timestamp}.json'
        backup_excel = f'form_responses_backup_{timestamp}.xlsx'
        
        # 備份JSON檔案
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            with open(backup_json, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 備份Excel檔案
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
            df.to_excel(backup_excel, index=False, engine='openpyxl')
        
        return jsonify({'success': True, 'filename': backup_excel})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/download')
def download_excel():
    if os.path.exists(EXCEL_FILE):
        return send_file(EXCEL_FILE, as_attachment=True)
    return jsonify({'error': 'No data available'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
