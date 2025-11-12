@echo off
echo 安装依赖包...
pip install -r requirements.txt

echo.
echo 启动表单服务器...
echo 表单地址: http://localhost:5000
echo 下载Excel: http://localhost:5000/download
echo 按 Ctrl+C 停止服务器
echo.

python server.py
pause
