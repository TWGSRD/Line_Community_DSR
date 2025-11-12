 -  1     : from flask import Flask, request, jsonify, send_from_directory
+       1: from flask import Flask, request, jsonify
   2,   2: import json
-  3     : import os
   4,   3: from datetime import datetime
   5,   4:
   6,   5: app = Flask(__name__)
+       6: data_store = []
   7,   7:
-  8     : # 使用全域變數存儲資料 (因為免費平台檔案系統限制)
-  9     : submissions_data = []
+       8: @app.route('/')
+       9: def home():
+      10:     return '''
+      11: <!DOCTYPE html>
+      12: <html lang="zh-TW">
+      13: <head>
+      14:     <meta charset="UTF-8">
+      15:     <meta name="viewport" content="width=device-width, initial-scale=1.0">
+      16:     <title>外部廠商資料填寫表單</title>
+      17:     <style>
+      18:         body { font-family: Arial, sans-serif; max-width: 700px; margin: 30px auto; padding: 20px; background: #f5f5f5; }
+      19:         .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
+      20:         h2 { color: #333; text-align: center; margin-bottom: 30px; }
+      21:         .form-group { margin-bottom: 20px; }
+      22:         label { display: block; margin-bottom: 8px; font-weight: bold; color: #555; }
+      23:         input, select, textarea { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 6px; font-size: 14px; box-sizing: border-box; }
+      24:         input:focus, select:focus, textarea:focus { border-color: #007cba; outline: none; }
+      25:         button { background: #007cba; color: white; padding: 12px 30px; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; width: 100%; }
+      26:         button:hover { background: #005a87; }
+      27:         .success { color: green; margin-top: 15px; padding: 10px; background: #d4edda; border-radius: 4px; }
+      28:         .error { color: red; margin-top: 15px; padding: 10px; background: #f8d7da; border-radius: 4px; }
+      29:         .required { color: red; }
+      30:     </style>
+      31: </head>
+      32: <body>
+      33:     <div class="container">
+      34:         <h2>外部廠商資料填寫表單</h2>
+      35:         <form id="dataForm">
+      36:             <div class="form-group">
+      37:                 <label for="company">公司名稱 <span class="required">*</span>：</label>
+      38:                 <input type="text" id="company" name="company" required>
+      39:             </div>
+      40:
+      41:             <div class="form-group">
+      42:                 <label for="contact_person">聯絡人姓名 <span class="required">*</span>：</label>
+      43:                 <input type="text" id="contact_person" name="contact_person" required>
+      44:             </div>
+      45:
+      46:             <div class="form-group">
+      47:                 <label for="email">電子郵件 <span class="required">*</span>：</label>
+      48:                 <input type="email" id="email" name="email" required>
+      49:             </div>
+      50:
+      51:             <div class="form-group">
+      52:                 <label for="phone">聯絡電話 <span class="required">*</span>：</label>
+      53:                 <input type="tel" id="phone" name="phone" required>
+      54:             </div>
+      55:
+      56:             <div class="form-group">
+      57:                 <label for="business_type">業務類型 <span class="required">*</span>：</label>
+      58:                 <select id="business_type" name="business_type" required>
+      59:                     <option value="">請選擇</option>
+      60:                     <option value="製造業">製造業</option>
+      61:                     <option value="貿易業">貿易業</option>
+      62:                     <option value="服務業">服務業</option>
+      63:                     <option value="科技業">科技業</option>
+      64:                     <option value="其他">其他</option>
+      65:                 </select>
+      66:             </div>
+      67:
+      68:             <div class="form-group">
+      69:                 <label for="services_needed">所需服務 <span class="required">*</span>：</label>
+      70:                 <textarea id="services_needed" name="services_needed" rows="3" placeholder="請描述您所需要的服務內容" required></textarea>
+      71:             </div>
+      72:
+      73:             <button type="submit">提交表單</button>
+      74:             <div id="message"></div>
+      75:         </form>
+      76:     </div>
  10,  77:
- 11     : @app.route('/')
- 12     : def index():
- 13     :     return send_from_directory('.', 'form.html')
+      78:     <script>
+      79:         document.getElementById('dataForm').addEventListener('submit', function(e) {
+      80:             e.preventDefault();
+      81:
+      82:             const formData = new FormData(this);
+      83:             const data = Object.fromEntries(formData);
+      84:
+      85:             fetch('/submit', {
+      86:                 method: 'POST',
+      87:                 headers: { 'Content-Type': 'application/json' },
+      88:                 body: JSON.stringify(data)
+      89:             })
+      90:             .then(response => response.json())
+      91:             .then(result => {
+      92:                 document.getElementById('message').innerHTML = '<div class="success">✓ 表單提交成功！感謝您的填寫。</div>';
+      93:                 this.reset();
+      94:             })
+      95:             .catch(error => {
+      96:                 document.getElementById('message').innerHTML = '<div class="error">✗ 提交失敗，請重試。</div>';
+      97:             });
+      98:         });
+      99:     </script>
+     100: </body>
+     101: </html>
+     102:     '''
  14, 103:
  15, 104: @app.route('/submit', methods=['POST'])
- 16     : def submit_form():
+     105: def submit():
  17, 106:     try:
- 18     :         data = request.json
+     107:         data = request.get_json()
  19, 108:         data['timestamp'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
- 20     :         data['submission_id'] = str(int(datetime.now().timestamp()))
- 21     :
- 22     :         # 存儲到記憶體
- 23     :         submissions_data.append(data)
- 24     :
- 25     :         # 嘗試寫入檔案 (如果平台支援)
- 26     :         try:
- 27     :             with open('submissions.json', 'w', encoding='utf-8') as f:
- 28     :                 json.dump(submissions_data, f, ensure_ascii=False, indent=2)
- 29     :         except:
- 30     :             pass  # 忽略檔案寫入錯誤
- 31     :
- 32     :         return jsonify({'status': 'success', 'message': '提交成功！'})
- 33     :     except Exception as e:
- 34     :         return jsonify({'status': 'error', 'message': f'提交失敗: {str(e)}'}), 500
+     109:         data_store.append(data)
+     110:         return jsonify({'status': 'success'})
+     111:     except:
+     112:         return jsonify({'status': 'error'}), 500
  35, 113:
  36, 114: @app.route('/admin')
  37, 115: def admin():
- 38     :     return f'''
- 39     :     <html>
- 40     :     <head><meta charset="UTF-8"><title>管理面板</title></head>
- 41     :     <body style="font-family: Arial; margin: 20px;">
- 42     :     <h2>提交記錄 ({len(submissions_data)} 筆)</h2>
- 43     :     {"".join([f"<div style='border:1px solid #ddd; padding:10px; margin:5px;'><strong>{item.get('company', '未填')}</strong> - {item.get('contact_person', '未填')}<br><small>{item.get('timestamp', '')}</small></div>" for item in submissions_data]) if submissions_data else "<p>暫無資料</p>"}
- 44     :     </body>
- 45     :     </html>
- 46     :     '''
+     116:     html = f'<h2>提交記錄 ({len(data_store)} 筆)</h2>'
+     117:     for item in data_store:
+     118:         html += f"<div style='border:1px solid #ddd; padding:10px; margin:5px;'><b>{item.get('company','')}</b> - {item.get('contact_person','')}<br>{item.get('timestamp','')}</div>"
+     119:     return html or '<p>暫無資料</p>'
  47, 120:
  48, 121: if __name__ == '__main__':
- 49     :     port = int(os.environ.get('PORT', 5000))
- 50     :     app.run(host='0.0.0.0', port=port, debug=False)
+     122:     app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))