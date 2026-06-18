@echo off
echo ========================================
echo   智慧学堂 - 本地启动服务器
echo ========================================
echo.
echo 正在启动 HTTP 服务器...
echo 浏览器将自动打开 http://localhost:3335
echo 按 Ctrl+C 停止服务器
echo.
start http://localhost:3335
python -m http.server 3335
pause
