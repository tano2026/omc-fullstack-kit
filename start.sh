#!/bin/bash
echo "========================================================"
echo "  KHOI DONG OMC MASTER QUAD-ENGINE & INGRESS GATEWAY"
echo "========================================================"
python3 skills/manager.py list
python3 gateway/telegram_gateway.py
