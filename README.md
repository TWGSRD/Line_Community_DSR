# 亞馬遜業務聯繫表單

## 功能特色
- 6個問題的表單系統
- 管理者密碼保護 (admin123)
- 資料自動儲存至Excel
- 網頁瀏覽提交資料
- 資料備份功能

## 本地運行
```bash
pip install -r requirements.txt
python server.py
```
訪問: http://localhost:5000

## 雲端部署
支援 Heroku、Railway、Render 等平台部署

## 檔案說明
- `server.py` - Flask後端服務器
- `form.html` - 表單前端頁面
- `form_config.json` - 表單配置檔案
- `requirements.txt` - Python依賴套件
- `Procfile` - 雲端部署配置

## 管理者功能
密碼: admin123
- 編輯表單問題
- 瀏覽提交資料
- 下載Excel檔案
- 資料備份
