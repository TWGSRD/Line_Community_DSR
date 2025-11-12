from flask import Flask, request, jsonify, send_file
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'submissions.json'

@app.route('/')
def index():
    return send_file('form.html')

@app.route('/test')
def test():
    return send_file('test.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # 獲取資料
        data = request.get_json()
        print(f"收到資料: {data}")
        
        # 讀取現有記錄
        records = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                records = json.load(f)
        
        # 添加新記錄
        records.append(data)
        
        # 儲存記錄
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        
        print(f"已儲存 {len(records)} 筆記錄")
        return jsonify({'status': 'success', 'count': len(records)})
        
    except Exception as e:
        print(f"錯誤: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/view')
def view_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                records = json.load(f)
            return jsonify(records)
        return jsonify([])
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("啟動簡化服務器...")
    print("表單: http://localhost:5000")
    print("測試: http://localhost:5000/test") 
    print("查看資料: http://localhost:5000/view")
    app.run(debug=True, host='0.0.0.0', port=5000)
