@echo off
chcp 65001 >nul
echo ======================================================
echo 🚀 OMC DEVELOPER SUPERPOWERS & HARNESS CLI
echo Workflow: /spec -^> /plan -^> /build -^> /review -^> /ship
echo ======================================================
if "%~1"=="" (
    python engines\harness\dev_harness.py --action all --task "Xây dựng tính năng mới cho OMC"
) else (
    python engines\harness\dev_harness.py %*
)
pause
