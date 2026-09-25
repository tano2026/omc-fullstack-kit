@echo off
chcp 65001 >nul
echo ======================================================
echo 🌐 DANG KHOI DONG GIAO DIEN OMC WEB CHAT & COMMAND CENTER
echo Dia chi: http://localhost:19888
echo ======================================================
start "" http://localhost:19888
python gateway\webhook_server.py
pause
