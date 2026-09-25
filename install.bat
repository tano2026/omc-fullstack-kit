@echo off
setlocal enabledelayedexpansion
title OMC Fullstack Master Kit - 1-Click Installer (Windows)

echo ======================================================================
echo    🏭 BO CAI DAT TU DONG OMC FULLSTACK MASTER KIT (WINDOWS)
echo    Bao gom: Quad-Engine (DSH + Hermes + OpenClaw 2.0 + JEV) + Obsidian
echo ======================================================================
echo.

:: 1. Kiem tra Python
echo [1/5] Kiem tra moi truong Python...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [X] Khong tim thay Python! Vui long cai dat Python 3.10+ tu https://www.python.org/
    echo     Hoac chay: winget install Python.Python.3.12
    pause
    exit /b 1
)
python --version

:: 2. Kiem tra Node.js & npm
echo.
echo [2/5] Kiem tra moi truong Node.js ^& npm...
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [X] Khong tim thay Node.js! Vui long cai dat Node.js 20+ tu https://nodejs.org/
    echo     Hoac chay: winget install OpenJS.NodeJS.LTS
    pause
    exit /b 1
)
node --version
npm --version

:: 3. Cai dat thu vien Python
echo.
echo [3/5] Cai dat cac goi thu vien Python (requirements.txt)...
python -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [!] Co canh bao khi cai thu vien Python, tiep tuc tien trinh...
) else (
    echo [OK] Thu vien Python da san sang.
)

:: 4. Kiem tra / Cai dat OpenClaw 2.0
echo.
echo [4/5] Kiem tra va cai dat OpenClaw 2.0 Engine...
where openclaw >nul 2>nul
if %errorlevel% neq 0 (
    echo [*] Dang cai dat OpenClaw 2.0 qua npm global...
    npm install -g openclaw@latest
) else (
    echo [OK] OpenClaw 2.0 da duoc cai dat:
    openclaw --version 2>nul
)

:: 5. Thiet lap file cau hinh .env
echo.
echo [5/5] Thiet lap file cau hinh moi truong...
if not exist "config\.env" (
    copy "config\.env.example" "config\.env" >nul
    echo [OK] Da khoi tao file config\.env tu template.
    echo     Hay dien OpenRouter API Key vao file config\.env de bot hoat dong.
) else (
    echo [OK] File config\.env da ton tai.
)

echo.
echo ======================================================================
echo    🎉 CAI DAT HOAN TAT THANH CONG!
echo ======================================================================
echo.
echo  Cac buoc tiep theo de bat dau:
echo   1. Mo 'copilot.bat' de chat truc tiep voi Hermes Master Co-Worker
echo   2. Mo 'start.bat' de bat Cổng Telegram Ingress Gateway 24/7
echo   3. Mo thu muc 'obsidian-vault\' bang ung dung Obsidian de xem Second Brain
echo   4. Chay 'python clone_company.py --name "Ten" --domain "Nganh"' de tao cong ty moi
echo.
pause
