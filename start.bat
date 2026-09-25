@echo off
title OMC Fullstack Master Kit - Ingress Gateway
echo ========================================================
echo   KHOI DONG OMC MASTER QUAD-ENGINE ^& INGRESS GATEWAY
echo ========================================================
echo.
echo 1. Kiem tra kho 700+ Skills...
python skills\manager.py list
echo.
echo 2. Khoi dong Telegram Ingress Gateway...
python gateway\telegram_gateway.py
pause
