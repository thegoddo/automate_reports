#!/usr/bin/env bash

# Daily Reports Cron Wrapper
# This script ensures proper environment setup before running the pipeline

export TZ=Asia/Kolkata
export ANTHROPIC_API_KEY="sk-ant-YOUR_API_KEY_HERE"  # Add your actual API key
export DATABASE_URL="postgresql://user:password@host:port/database"  # Add your DB credentials

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$BASE_DIR/logs/cron.log"

mkdir -p "$BASE_DIR/logs"

{
    echo "========================================"
    echo "Cron run started: $(date)"
    echo "========================================"

    cd "$BASE_DIR" && bash "$BASE_DIR/daily_report.sh"

    echo ""
    echo "========================================"
    echo "Cron run completed: $(date)"
    echo "========================================"
} >> "$LOG_FILE" 2>&1
