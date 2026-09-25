#!/bin/bash
echo "======================================================"
echo "🌐 DANG KHOI DONG GIAO DIEN OMC WEB CHAT & COMMAND CENTER"
echo "Dia chi: http://localhost:19888"
echo "======================================================"
which xdg-open > /dev/null && xdg-open http://localhost:19888 || open http://localhost:19888 2>/dev/null || true
python3 gateway/webhook_server.py
