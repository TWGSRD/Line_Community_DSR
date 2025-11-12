   1,  1: from flask import Flask, request, jsonify, send_from_directory
   2,  2: import json
   3,  3: import os
   4,  4: from datetime import datetime
   5,  5:
   6,  6: app = Flask(__name__)
   7,  7:
+      8: # 使用全域變數存儲資料 (因為免費平台檔案系統限制)
+      9: submissions_data = []
+     10:
   8, 11: @app.route('/')
   9, 12: def index():
  10, 13:     return send_from_directory('.', 'form.html')
  11, 14:
  12, 15: @app.route('/submit', methods=['POST'])
  13, 16: def submit_form():
  14, 17:     try:
  15, 18:         data = request.json
  16, 19:         data['timestamp'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
  17, 20:         data['submission_id'] = str(int(datetime.now().timestamp()))
  18, 21:
- 19    :         # 使用環境變量或簡單文件存儲
- 20    :         filename = 'submissions.json'
- 21    :         if os.path.exists(filename):
- 22    :             with open(filename, 'r', encoding='utf-8') as f:
- 23    :                 records = json.load(f)
- 24    :         else:
- 25    :             records = []
+     22:         # 存儲到記憶體
+     23:         submissions_data.append(data)
  26, 24:
- 27    :         records.append(data)
+     25:         # 嘗試寫入檔案 (如果平台支援)
+     26:         try:
+     27:             with open('submissions.json', 'w', encoding='utf-8') as f:
+     28:                 json.dump(submissions_data, f, ensure_ascii=False, indent=2)
+     29:         except:
+     30:             pass  # 忽略檔案寫入錯誤
  28, 31:
- 29    :         with open(filename, 'w', encoding='utf-8') as f:
- 30    :             json.dump(records, f, ensure_ascii=False, indent=2)
- 31    :
- 32    :         return jsonify({'status': 'success'})
+     32:         return jsonify({'status': 'success', 'message': '提交成功！'})
  33, 33:     except Exception as e:
- 34    :         return jsonify({'status': 'error', 'message': str(e)}), 500
+     34:         return jsonify({'status': 'error', 'message': f'提交失敗: {str(e)}'}), 500
+     35:
+     36: @app.route('/admin')
+     37: def admin():
+     38:     return f'''
+     39:     <html>
+     40:     <head><meta charset="UTF-8"><title>管理面板</title></head>
+     41:     <body style="font-family: Arial; margin: 20px;">
+     42:     <h2>提交記錄 ({len(submissions_data)} 筆)</h2>
+     43:     {"".join([f"<div style='border:1px solid #ddd; padding:10px; margin:5px;'><strong>{item.get('company', '未填')}</strong> - {item.get('contact_person', '未填')}<br><small>{item.get('timestamp', '')}</small></div>" for item in submissions_data]) if submissions_data else "<p>暫無資料</p>"}
+     44:     </body>
+     45:     </html>
+     46:     '''
  35, 47:
  36, 48: if __name__ == '__main__':
  37, 49:     port = int(os.environ.get('PORT', 5000))
- 38    :     app.run(host='0.0.0.0', port=port)
+     50:     app.run(host='0.0.0.0', port=port, debug=False)