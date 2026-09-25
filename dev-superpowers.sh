#!/bin/bash
echo "======================================================"
echo "🚀 OMC DEVELOPER SUPERPOWERS & HARNESS CLI"
echo "Workflow: /spec -> /plan -> /build -> /review -> /ship"
echo "======================================================"
if [ -z "$1" ]; then
    python3 engines/harness/dev_harness.py --action all --task "Xây dựng tính năng mới cho OMC"
else
    python3 engines/harness/dev_harness.py "$@"
fi
