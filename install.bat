@echo off
setlocal enabledelayedexpansion
title OMC Fullstack Master Kit - 1-Click Installer (Windows)

echo ======================================================================
echo    🏭 BO CAI DAT TU DONG OMC FULLSTACK MASTER KIT (WINDOWS)
echo    Bao gom: Quad-Engine (DSH + Hermes + OpenClaw 2.0 + JEV)
echo    Dac biet: Superpowers Dev Suite + Harness Evals + Obsidian Second Brain
echo ======================================================================
echo.

:: 1. Kiem tra Python
echo [1/6] Kiem tra moi truong Python...
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
echo [2/6] Kiem tra moi truong Node.js ^& npm...
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
echo [3/6] Cai dat cac goi thu vien Python (requirements.txt)...
python -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [!] Co canh bao khi cai thu vien Python, tiep tuc tien trinh...
) else (
    echo [OK] Thu vien Python da san sang (bao gom filelock, fastapi, pydantic).
)

:: 4. Kiem tra / Cai dat OpenClaw 2.0 & PM2
echo.
echo [4/6] Kiem tra OpenClaw 2.0 ^& PM2 Supervisor...
where openclaw >nul 2>nul
if %errorlevel% neq 0 (
    echo [*] Dang cai dat OpenClaw 2.0 qua npm global...
    npm install -g openclaw@latest
) else (
    echo [OK] OpenClaw 2.0 da duoc cai dat.
)

where pm2 >nul 2>nul
if %errorlevel% neq 0 (
    echo [*] Dang cai dat PM2 de giam sat tien trinh tu dong 24/7...
    npm install -g pm2
) else (
    echo [OK] PM2 Supervisor da san sang.
)

:: 5. Thiet lap file cau hinh .env & Kiem tra Bao mat JEV
echo.
echo [5/6] Thiet lap file cau hinh .env va kiem tra bao mat Zero-Damage...
if not exist "config\.env" (
    copy "config\.env.example" "config\.env" >nul
    echo [OK] Da khoi tao file config\.env tu template.
    echo     Hay dien OpenRouter API Key vao file config\.env de bot hoat dong.
) else (
    echo [OK] File config\.env da ton tai.
)

python engines\jev_gateway\safety_guard.py >nul 2>nul
if %errorlevel% equ 0 (
    echo [OK] JEV Sentinel Safety Gatekeeper hoat dong tot.
)

:: 6. Kiem tra Dev Superpowers & Harness
echo.
echo [6/6] Kiem tra Developer Superpowers ^& Harness Engine...
python engines\harness\dev_harness.py --action eval >nul 2>nul
if %errorlevel% equ 0 (
    echo [OK] Dev Superpowers (/spec, /plan, /build, /review, /ship) san sang 100%%.
)

echo.
echo ======================================================================
echo    🎉 CAI DAT HOAN TAT THANH CONG!
echo ======================================================================
echo.
echo CAC LENH KHOI DONG NHANH:
echo   1. Tro ly Hermes Master Copilot :  copilot.bat
echo   2. Developer Superpowers ^& Harness:  dev-superpowers.bat
echo   3. Khoi dong Telegram Gateway  :  start.bat
echo   4. Chay 24/7 bang PM2          :  npm run pm2:start
echo   5. Nhan ban cong ty moi        :  python clone_company.py
echo.
pause
