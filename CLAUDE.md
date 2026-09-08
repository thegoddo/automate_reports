# Automated Daily Reports System

## Overview

This project automates the generation and distribution of daily feedback reports. It orchestrates a three-stage pipeline:

1. **Database Extraction** - SQL queries extract feedback data from PostgreSQL
2. **AI Analysis** - Claude API analyzes CSV data and generates insights
3. **Distribution** - Reports are sent to WhatsApp groups

## Architecture

```
PostgreSQL Database
        ↓
   SQL Queries (queries/*.sql)
        ↓
   CSV Files (output/{date}/*.csv)
        ↓
   Claude API Analysis (generate_report.py)
        ↓
   Report Text (output/{date}/*.txt)
        ↓
   WhatsApp Distribution (whatsapp.py)
```

## Project Structure

```
automate_reports/
├── automate_reports.sh         # Main orchestrator script
├── daily_report.sh             # Alternative entry point
├── generate_report.py          # Claude API integration
├── whatsapp.py                 # WhatsApp distribution
├── whatsapp_group.json         # WhatsApp group IDs and mappings
├── requirements.txt            # Python dependencies
├── queries/                    # SQL query files
│   ├── feedback_totals.sql
│   ├── manager_breakdown.sql
│   ├── issue_summary.sql
│   ├── top_issues.sql
│   ├── issue_details.sql
│   ├── compliment_counts.sql
│   └── compliment_details.sql
├── config/                     # Configuration directory
├── output/                     # Generated reports (date-organized)
│   └── {YYYY-MM-DD}/
│       ├── feedback_totals.csv/txt
│       ├── manager_breakdown.csv/txt
│       └── ...
├── logs/                       # Execution logs
└── reports/                    # Report templates/storage
```

## Key Files

### `automate_reports.sh`
Main orchestrator that runs SQL queries and extracts data into CSVs.

**Env vars required:**
- `DATABASE_URL` - PostgreSQL connection string

**Output:** CSVs for each report type dated by yesterday's date in Asia/Kolkata timezone

### `generate_report.py`
Uses Claude API to analyze CSV files and generate text reports.

**Env vars required:**
- `ANTHROPIC_API_KEY` - Claude API key

**Model:** `claude-sonnet-5` (configurable via `CLAUDE_MODEL` constant)

**Max tokens:** 4096 (configurable via `MAX_TOKENS` constant)

**Reports generated:**
- `feedback_totals` - Total feedback per outlet
- `manager_breakdown` - Feedback analysis by manager
- `issue_summary` - Issues by severity and status
- `top_issues` - Most frequent issues ranked
- `issue_details` - Detailed issue narrative with context
- `compliment_counts` - Positive feedback summary
- `compliment_details` - Detailed compliments by category

### `whatsapp.py`
Sends generated reports to WhatsApp groups using WhatsApp Web automation.

**Env vars required:** None (but requires WhatsApp Web access)

**Config file:** `whatsapp_group.json` (root directory)
```json
{
  "feedback_totals": "BmXPTGGbTxt3yMv5L4VNtb",
  "manager_breakdown": "ANOTHER_GROUP_ID",
  "issue_summary": "ISSUES_GROUP_ID",
  "top_issues": "ISSUES_GROUP_ID",
  "issue_details": "ISSUES_GROUP_ID",
  "compliment_counts": "COMPLIMENTS_GROUP_ID",
  "compliment_details": "COMPLIMENTS_GROUP_ID"
}
```

**Note:** This script uses PyAutoGUI to automate browser interactions. It requires:
- Chrome/Firefox with WhatsApp Web open
- 15-second wait time for page load (configurable via `WAIT_TIME`)
- Automatic tab closure after sending (configurable via `CLOSE_TAB`)

## Setup & Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- `anthropic` - Claude API client
- `pyperclip` - Clipboard management for WhatsApp
- `pywhatkit` - WhatsApp Web integration
- `pyautogui` - Browser automation

### 2. Set Environment Variables

```bash
export DATABASE_URL="postgresql://user:password@host:port/database"
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 3. Configure WhatsApp Groups

Update `whatsapp_group.json` in the root directory with actual group IDs:
```json
{
  "feedback_totals": "YOUR_GROUP_ID_1",
  "manager_breakdown": "YOUR_GROUP_ID_2",
  "issue_summary": "YOUR_GROUP_ID_3",
  "top_issues": "YOUR_GROUP_ID_4",
  "issue_details": "YOUR_GROUP_ID_5",
  "compliment_counts": "YOUR_GROUP_ID_6",
  "compliment_details": "YOUR_GROUP_ID_7"
}
```

**Note:** Replace placeholder IDs with actual WhatsApp group IDs. Group IDs can be found using pywhatkit tools or extracted from WhatsApp Web API calls.

## Running the Project

### Full Automation (All 3 Stages)
```bash
./daily_report.sh
```

### Individual Stages
```bash
# Stage 1: Extract from database
./automate_reports.sh

# Stage 2: Generate Claude reports (requires CSVs from stage 1)
python3 generate_report.py

# Stage 3: Send to WhatsApp (requires TXT reports from stage 2)
python3 whatsapp.py
```

## Scheduling

Add to crontab to run daily at 8 AM (Asia/Kolkata):
```bash
0 2 * * * TZ=Asia/Kolkata /path/to/automate_reports/daily_report.sh >> /path/to/automate_reports/logs/daily.log 2>&1
```

**Note:** Cron offset = UTC 2:30 AM for 8 AM IST (adjust for daylight savings)

## Development Guidelines

### Adding a New Report

1. **Create SQL query** in `queries/new_report_name.sql`
   - Use `:report_date` variable for filtering by date
   - Output must be CSV format

2. **Add to REPORTS dict** in `generate_report.py`
   ```python
   "new_report_name": {
       "prompt": """Your analysis instructions here."""
   }
   ```

3. **Add to orchestrator** in `automate_reports.sh`
   ```bash
   REPORTS=(
       ...
       "new_report_name"
   )
   ```

4. **Configure WhatsApp** in `config/whatsapp_groups.json`
   ```json
   {
       "new_report_name": "group-id"
   }
   ```

### Modifying Report Prompts

Edit the `prompt` field in the `REPORTS` dict in `generate_report.py`. Prompts should:
- Be specific about required analysis
- Explicitly forbid inventing/assuming data
- Instruct to return only report text
- Reference relevant columns from CSV

### Debugging

**Database extraction issues:**
- Verify `DATABASE_URL` is set: `echo $DATABASE_URL`
- Test SQL manually: `psql $DATABASE_URL -f queries/feedback_totals.sql`
- Check logs: `cat logs/`

**Claude API issues:**
- Verify `ANTHROPIC_API_KEY` is set: `echo $ANTHROPIC_API_KEY | head -c 20`
- Check for file existence: `ls -la output/{date}/`
- Test single report: `python3 generate_report.py`

**WhatsApp issues:**
- Ensure WhatsApp Web is open in browser
- Verify group IDs in `whatsapp_group.json`
- Check that PyAutoGUI can control mouse (X11 on Linux)
- Test manually: run script and observe browser automation

## Environment Variables

| Variable | Required | Example | Purpose |
|----------|----------|---------|---------|
| `DATABASE_URL` | Yes | `postgresql://user:pass@localhost/db` | PostgreSQL connection |
| `ANTHROPIC_API_KEY` | Yes | `sk-ant-...` | Claude API authentication |
| `TZ` | No | `Asia/Kolkata` | Timezone for report date |

## Error Handling

All scripts use `set -euo pipefail` (bash) to fail fast on errors. This means:
- Script exits immediately on command failure
- Undefined variables cause errors
- Pipe failures are caught

Python scripts validate:
- Required environment variables
- File existence and readability
- Claude API responses
- CSV content non-empty

## Performance Notes

- Database queries: Time depends on feedback volume
- Claude API calls: ~5-10 seconds per report (7 reports = ~1 minute)
- WhatsApp sending: ~3 seconds per report (7 reports = ~30 seconds)
- **Total runtime:** ~2-3 minutes for full pipeline

## Troubleshooting

**"ANTHROPIC_API_KEY is not set"**
- Run: `export ANTHROPIC_API_KEY='your-key'`
- Add to shell profile for persistence

**"Output directory does not exist"**
- Stage 1 (automate_reports.sh) must run before stage 2
- Check logs for SQL query failures

**"Claude returned an empty response"**
- Check CSV content is valid
- Verify prompt instructions are sound
- Check Claude API rate limits

**WhatsApp authentication fails**
- Login to WhatsApp Web manually first
- Ensure session is active
- Check browser permissions for clipboard access

## Dependencies

See `requirements.txt` for Python packages. Also requires:
- PostgreSQL client (`psql`)
- Python 3.8+
- Chrome or Firefox (for WhatsApp Web)
- X11 or Wayland (for PyAutoGUI on Linux)

## Related Files

- **SQL Queries:** `queries/` directory contains all data extraction logic
- **Test Data:** `test/` directory contains development test files
- **Configuration:** `whatsapp_group.json` maps reports to WhatsApp groups
- **Reports Storage:** `reports/` directory for report templates/archives

## Future Improvements

- [ ] Support for multiple messaging platforms (Slack, Teams, Email)
- [ ] Report caching to avoid re-processing
- [ ] Email delivery as alternative to WhatsApp
- [ ] Custom report scheduling (not just daily)
- [ ] Report versioning and archival
- [ ] Automated testing framework
