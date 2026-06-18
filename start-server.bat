@echo off
chcp 65001 >nul
echo ========================================
echo   智慧学堂 - 本地启动服务器
echo ========================================
echo.
echo 正在启动 Node.js 服务器...
echo 浏览器将自动打开 http://localhost:3000
echo 按 Ctrl+C 停止服务器
echo.
set NODE_OPTIONS=
start http://localhost:3000
node server.js
pause
