#!/usr/bin/env bash

set -euo pipefail

# ============================================================
# DAILY FEEDBACK REPORT - DATABASE EXTRACTION
# ============================================================

# Yesterday's date in Asia/Kolkata
REPORT_DATE=$(TZ=Asia/Kolkata date -d "yesterday" +%Y-%m-%d)

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUERY_DIR="$BASE_DIR/queries"
OUTPUT_DIR="$BASE_DIR/output/$REPORT_DATE"
LOG_DIR="$BASE_DIR/logs"

mkdir -p "$OUTPUT_DIR" "$LOG_DIR"

REPORTS=(
    "feedback_totals"
    "manager_breakdown"
    "issue_summary"
    "top_issues"
    "issue_details"
    "compliment_counts"
    "compliment_details"
)

echo "========================================"
echo "Daily Feedback Report - Database"
echo "Report date: $REPORT_DATE"
echo "Started: $(date)"
echo "========================================"

for report in "${REPORTS[@]}"; do

    echo ""
    echo "Running query: $report"

    psql "$DATABASE_URL" \
        -v ON_ERROR_STOP=1 \
        -v report_date="$REPORT_DATE" \
        --csv \
        -f "$QUERY_DIR/$report.sql" \
        > "$OUTPUT_DIR/$report.csv"

    echo "Completed: $report"
    echo "Output: $OUTPUT_DIR/$report.csv"

done

echo ""
echo "========================================"
echo "All database queries completed."
echo "Finished: $(date)"
echo "Output directory: $OUTPUT_DIR"
echo "========================================"
