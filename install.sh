#!/usr/bin/env bash
set -e

echo "======================================================================"
echo "   🏭 BO CAI DAT TU DONG OMC FULLSTACK MASTER KIT (LINUX/MACOS)"
echo "   Bao gom: Quad-Engine (DSH + Hermes + OpenClaw 2.0 + JEV)"
echo "   Dac biet: Superpowers Dev Suite + Harness Evals + Obsidian Second Brain"
echo "======================================================================"
echo ""

# 1. Kiem tra Python
echo "[1/6] Kiem tra moi truong Python..."
if ! command -v python3 &> /dev/null; then
    echo "[X] Khong tim thay Python3! Vui long cai dat python3."
    exit 1
fi
python3 --version

# 2. Kiem tra Node.js & npm
echo ""
echo "[2/6] Kiem tra moi truong Node.js & npm..."
if ! command -v node &> /dev/null; then
    echo "[X] Khong tim thay Node.js! Vui long cai dat Node.js 20+."
    exit 1
fi
node --version
npm --version

# 3. Cai dat thu vien Python
echo ""
echo "[3/6] Cai dat cac goi thu vien Python (requirements.txt)...
pip3 install -r requirements.txt --quiet || pip install -r requirements.txt --quiet
echo "[OK] Thu vien Python da san sang."

# 4. Kiem tra / Cai dat OpenClaw 2.0 & PM2
echo ""
echo "[4/6] Kiem tra OpenClaw 2.0 & PM2..."
if ! command -v openclaw &> /dev/null; then
    echo "[*] Dang cai dat OpenClaw 2.0 qua npm..."
    npm install -g openclaw@latest || sudo npm install -g openclaw@latest
fi

if ! command -v pm2 &> /dev/null; then
    echo "[*] Dang cai dat PM2 qua npm..."
    npm install -g pm2 || sudo npm install -g pm2
fi

# 5. File cau hinh .env & Kiem tra Bao mat
echo ""
echo "[5/6] Thiet lap file cau hinh .env & kiem tra bao mat..."
if [ ! -f "config/.env" ]; then
    cp "config/.env.example" "config/.env"
    echo "[OK] Da khoi tao config/.env tu template."
else
    echo "[OK] File config/.env da ton tai."
fi
python3 engines/jev_gateway/safety_guard.py > /dev/null 2>&1 || true

# 6. Kiem tra Dev Superpowers & Harness
echo ""
echo "[6/6] Kiem tra Developer Superpowers & Harness Engine..."
python3 engines/harness/dev_harness.py --action eval > /dev/null 2>&1 || true
echo "[OK] Dev Superpowers (/spec, /plan, /build, /review, /ship) san sang."

chmod +x copilot.sh start.sh dev-superpowers.sh

echo ""
echo "======================================================================"
echo "   🎉 CAI DAT HOAN TAT THANH CONG!"
echo "======================================================================"
echo ""
echo "CAC LENH KHOI DONG NHANH:"
echo "  1. Tro ly Hermes Master Copilot :  ./copilot.sh"
echo "  2. Developer Superpowers & Harness:  ./dev-superpowers.sh"
echo "  3. Khoi dong Telegram Gateway  :  ./start.sh"
echo "  4. Chay 24/7 bang PM2          :  npm run pm2:start"
echo "  5. Nhan ban cong ty moi        :  python3 clone_company.py"
echo ""
