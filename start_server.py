#!/usr/bin/env python3
import subprocess
import sys
import os

# 切換到正確目錄
os.chdir(r'C:\Users\vikao\Desktop\Nurturing Group')

print("正在啟動表單服務器...")
print("請在瀏覽器訪問: http://localhost:5000")
print("按 Ctrl+C 停止服務器")
print("-" * 50)

try:
    # 啟動服務器
    subprocess.run([sys.executable, 'server.py'], check=True)
except KeyboardInterrupt:
    print("\n服務器已停止")
except Exception as e:
    print(f"啟動失敗: {e}")
    input("按Enter鍵退出...")
