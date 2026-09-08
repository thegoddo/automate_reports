# 📊 Automated Daily Reports

Automate the generation and distribution of daily feedback reports. This system extracts feedback data from PostgreSQL, analyzes it using Claude AI, and sends insights to WhatsApp groups.

## ✨ Features

- **Automated Data Extraction** - SQL queries pull feedback data from PostgreSQL daily
- **AI-Powered Analysis** - Claude API generates insights and summaries from raw data
- **Multi-Report Generation** - 7 different report types covering feedback, issues, and compliments
- **WhatsApp Distribution** - Automatically sends reports to designated group chats
- **Timezone-Aware** - Operates in Asia/Kolkata timezone by default
- **Error Handling** - Graceful failure modes with detailed logging
- **Extensible** - Easy to add new report types and distribution channels

## 📋 Report Types

The system generates 7 daily reports:

1. **Feedback Totals** - Total feedback per outlet with rankings
2. **Manager Breakdown** - Feedback analysis by manager
3. **Issue Summary** - Issues grouped by severity and status
4. **Top Issues** - Most frequently reported problems ranked
5. **Issue Details** - Detailed issue narrative with corrective actions
6. **Compliment Counts** - Positive feedback summary
7. **Compliment Details** - Specific compliments by category (food, ambience, service)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- PostgreSQL with feedback data
- Claude API key (from Anthropic)
- Chrome/Firefox with WhatsApp Web access

### 1. Clone & Install

```bash
cd automate_reports
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
export DATABASE_URL="postgresql://user:password@host:port/database"
export ANTHROPIC_API_KEY="sk-ant-your-api-key-here"
```

### 3. Update WhatsApp Groups

Edit `whatsapp_group.json` with your group IDs:

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

### 4. Run the Pipeline

```bash
# Full automation (all 3 stages)
./daily_report.sh

# Or individual stages
./automate_reports.sh          # Stage 1: Extract data
python3 generate_report.py     # Stage 2: Generate reports
python3 whatsapp.py            # Stage 3: Send reports
```

## 📁 Project Structure

```
automate_reports/
├── README.md                  # This file
├── CLAUDE.md                  # Detailed development guide
├── automate_reports.sh        # Database extraction
├── daily_report.sh            # Full pipeline orchestrator
├── generate_report.py         # Claude AI report generation
├── whatsapp.py                # WhatsApp distribution
├── whatsapp_group.json        # WhatsApp group configuration
├── requirements.txt           # Python dependencies
├── queries/                   # SQL query files
├── config/                    # Configuration directory
├── output/                    # Generated reports (date-organized)
├── logs/                      # Execution logs
└── reports/                   # Report archives
```

## ⚙️ Configuration

### Database Connection

Set `DATABASE_URL` with your PostgreSQL credentials:

```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/database_name"
```

### Claude API Settings

**API Key:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Model & Tokens** (in `generate_report.py`):
```python
CLAUDE_MODEL = "claude-sonnet-5"  # Change to claude-opus-5 for better quality
MAX_TOKENS = 4096                # Adjust based on report complexity
```

### WhatsApp Groups

Get group IDs from WhatsApp Web:
1. Open WhatsApp Web (web.whatsapp.com)
2. Open DevTools (F12)
3. In Console: inspect network requests to WhatsApp API
4. Copy group IDs to `whatsapp_group.json`

## 📅 Scheduling

### Run Daily at 8 AM (IST)

Add to crontab:

```bash
crontab -e

# Add this line (runs at 2:30 AM UTC = 8 AM IST)
0 2 * * * TZ=Asia/Kolkata /path/to/automate_reports/daily_report.sh >> /path/to/automate_reports/logs/daily.log 2>&1
```

### Check Crontab

```bash
crontab -l
```

## 🔧 Usage Examples

### Run Full Pipeline

```bash
./daily_report.sh
```

Output:
```
========================================
DAILY FEEDBACK AUTOMATION
Started: Tue Sep 8 02:30:00 UTC 2026
========================================

[1/3] Running PostgreSQL queries...
[2/3] Generating Claude reports...
[3/3] Sending reports to WhatsApp...

========================================
DAILY REPORT COMPLETED SUCCESSFULLY
Finished: Tue Sep 8 02:33:15 UTC 2026
========================================
```

### Run Specific Stage

```bash
# Extract data only
./automate_reports.sh

# Generate reports only (requires CSVs)
python3 generate_report.py

# Send reports only (requires TXT files)
python3 whatsapp.py
```

### View Report Output

```bash
# Today's reports
ls -la output/2026-09-08/

# View a specific report
cat output/2026-09-08/feedback_totals.txt

# View logs
tail -f logs/daily.log
```

## 🐛 Troubleshooting

### "ANTHROPIC_API_KEY is not set"

Make sure the environment variable is set:
```bash
echo $ANTHROPIC_API_KEY  # Should print your API key

# If empty, run:
export ANTHROPIC_API_KEY="sk-ant-..."
```

### "Output directory does not exist"

Run database extraction first:
```bash
./automate_reports.sh
```

Then check the output:
```bash
ls -la output/
```

### WhatsApp Reports Not Sending

1. **Verify WhatsApp Web is active:**
   - Open web.whatsapp.com in browser
   - Ensure you're logged in

2. **Check group IDs:**
   ```bash
   cat whatsapp_group.json
   ```

3. **Test with a single report:**
   ```bash
   python3 -c "from whatsapp import send_report; send_report('feedback_totals', 'YOUR_GROUP_ID')"
   ```

4. **Check PyAutoGUI permissions (Linux):**
   ```bash
   # Ensure X11 forwarding is working
   echo $DISPLAY
   ```

### Claude API Errors

Check API limits and billing:
- Visit: https://console.anthropic.com
- Check rate limits and quota
- Verify API key is valid

### Database Connection Issues

Test connection:
```bash
psql $DATABASE_URL -c "SELECT COUNT(*) FROM feedback;"
```

## 📊 Output Format

### CSV Format (Stage 1)

```
output/2026-09-08/feedback_totals.csv
outlet,total_feedback,status
Outlet A,145,active
Outlet B,98,active
```

### Report Format (Stage 2)

```
output/2026-09-08/feedback_totals.txt
DAILY FEEDBACK REPORT - 2026-09-08

Total Feedback Summary:
- Outlet A: 145 feedback entries
- Outlet B: 98 feedback entries
- Outlet C: 87 feedback entries
...
```

## 🔐 Security Notes

- **API Keys:** Use environment variables, never hardcode
- **Database:** Use strong passwords, restrict network access
- **WhatsApp:** Session tokens are handled by browser, not stored
- **Logs:** Review logs regularly for errors or suspicious activity

## 📝 Environment Variables

| Variable | Required | Example |
|----------|----------|---------|
| `DATABASE_URL` | Yes | `postgresql://user:pass@localhost/db` |
| `ANTHROPIC_API_KEY` | Yes | `sk-ant-...` |
| `TZ` | No | `Asia/Kolkata` |

## 🤝 Contributing

To add a new report type:

1. **Create SQL query** in `queries/new_report.sql`
2. **Add to REPORTS dict** in `generate_report.py`
3. **Update orchestrator** in `automate_reports.sh`
4. **Configure WhatsApp** in `whatsapp_group.json`
5. **Test thoroughly** before scheduling

See `CLAUDE.md` for detailed development guidelines.

## 📖 Documentation

- **CLAUDE.md** - Comprehensive development guide
- **README.md** - This file (user-focused)
- **queries/*.sql** - SQL query documentation
- **Log files** - Debug logs in `logs/` directory

## ⏱️ Performance

- **Database queries:** 1-2 minutes (depends on data volume)
- **Claude API calls:** 1-2 minutes (7 reports)
- **WhatsApp sending:** ~30 seconds (7 reports)
- **Total runtime:** ~2-3 minutes

## 🆘 Support

For issues or questions:

1. Check `CLAUDE.md` for detailed troubleshooting
2. Review log files in `logs/` directory
3. Verify all environment variables are set
4. Test individual stages independently
5. Check database and API connectivity

## 📄 License

This project is part of FigitaLabs automation suite.

## 🎯 Future Enhancements

- [ ] Email distribution
- [ ] Slack integration
- [ ] Custom report scheduling
- [ ] Web dashboard for historical reports
- [ ] Automated testing suite
- [ ] Report versioning and archival
- [ ] Multi-outlet support
- [ ] Report customization by group

---

**Last Updated:** 2026-09-08  
**Timezone:** Asia/Kolkata (IST)  
**Version:** 1.0
