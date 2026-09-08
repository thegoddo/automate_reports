#!/usr/bin/env bash

set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$BASE_DIR/logs"

mkdir -p "$LOG_DIR"

echo "========================================"
echo "DAILY FEEDBACK AUTOMATION"
echo "Started: $(date)"
echo "========================================"

echo ""
echo "[1/3] Running PostgreSQL queries..."
"$BASE_DIR/automate_reports.sh"

echo ""
echo "[2/3] Generating Claude reports..."
python3 "$BASE_DIR/generate_report.py"

echo ""
echo "[3/3] Sending reports to WhatsApp..."
python3 "$BASE_DIR/whatsapp.py"

echo ""
echo "========================================"
echo "DAILY REPORT COMPLETED SUCCESSFULLY"
echo "Finished: $(date)"
echo "========================================"
