#!/usr/bin/env python3

import os
from datetime import date, timedelta
from pathlib import Path

import anthropic


# ============================================================
# CONFIGURATION
# ============================================================

CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")

CLAUDE_MODEL = "claude-sonnet-5"

MAX_TOKENS = 4096


# ============================================================
# REPORT CONFIGURATION
# ============================================================
#
# Every report:
#
#   CSV -> Claude -> TXT
#
# Each report has its own prompt.
# ============================================================

REPORTS = {
    "feedback_totals": {
        "prompt": """
Analyze the feedback totals data provided below.

Create a concise daily report containing:

- Total feedback for each outlet
- Outlet with the highest feedback
- Outlet with the lowest feedback
- Any notable differences between outlets

Use only the information provided in the CSV.

Do not invent or assume any information.

Return only the final report text.
"""
    },

    "manager_breakdown": {
        "prompt": """
Analyze the manager-wise feedback data provided below.

Create a concise report containing:

- Feedback count for each manager
- Managers with the highest feedback volume
- Managers with the lowest feedback volume
- Any notable patterns between managers or outlets

Use only the information provided in the CSV.

Do not invent or assume any information.

Return only the final report text.
"""
    },

    "issue_summary": {
        "prompt": """
Analyze the issue summary data provided below.

Focus on:

- Medium severity issues
- High severity issues
- Pending issues
- Resolved issues
- Total feedback containing issues
- Outlets with the highest issue counts
- Important operational observations

Clearly identify the most significant problem areas.

Use only the information provided in the CSV.

Do not invent or assume any information.

Return only the final report text.
"""
    },

    "top_issues": {
        "prompt": """
Analyze the top issues data provided below.

Identify the most frequently reported Medium and High severity issues.

For the important issues, include:

- Outlet
- Category
- Attribute / issue
- Severity
- Number of mentions

Rank the issues by importance and frequency.

Use only the information provided in the CSV.

Do not invent or assume any information.

Return only the final report text.
"""
    },

    "issue_details": {
        "prompt": """
Analyze the detailed issue data provided below.

Create a useful narrative of the major customer issues.

For each important issue, consider:

- Outlet
- Manager
- Issue description
- Category
- Severity
- Current status
- Corrective action

Focus on recurring and actionable problems.

Group similar issues where appropriate.

Use only the information provided in the CSV.

Do not invent or assume any information.

Return only the final report text.
"""
    },

    "compliment_counts": {
        "prompt": """
Analyze the compliment counts provided below.

Create a concise positive-feedback report covering:

- Food compliments
- Ambience compliments
- Service compliments
- Outlet-wise differences
- Outlets receiving the most positive mentions

Use only the information provided in the CSV.

Do not invent or assume any information.

Return only the final report text.
"""
    },

    "compliment_details": {
        "prompt": """
Analyze the detailed customer compliments provided below.

Summarize meaningful positive feedback relating to:

- Food
- Ambience
- Service

Highlight specific dishes, services, experiences, or aspects that customers appreciated.

Group similar compliments where appropriate.

Ignore meaningless or extremely generic entries where possible.

Use only the information provided in the CSV.

Do not invent or assume any information.

Return only the final report text.
"""
    },
}


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

# Always generate the report for yesterday.
REPORT_DATE = (
    date.today() - timedelta(days=1)
).isoformat()

OUTPUT_DIR = BASE_DIR / "output" / REPORT_DATE


# ============================================================
# VALIDATION
# ============================================================

def validate_configuration():
    """Validate required configuration before starting."""

    if not CLAUDE_API_KEY:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set.\n"
            "Run:\n"
            "export ANTHROPIC_API_KEY='your-api-key'"
        )

    if not OUTPUT_DIR.exists():
        raise FileNotFoundError(
            f"Output directory does not exist:\n{OUTPUT_DIR}\n\n"
            "Run run_reports.sh first."
        )


# ============================================================
# READ CSV
# ============================================================

def read_csv(report_name: str) -> str:
    """Read the CSV belonging to a report."""

    csv_file = OUTPUT_DIR / f"{report_name}.csv"

    if not csv_file.exists():
        raise FileNotFoundError(
            f"CSV file not found:\n{csv_file}"
        )

    csv_content = csv_file.read_text(
        encoding="utf-8"
    ).strip()

    if not csv_content:
        raise RuntimeError(
            f"CSV file is empty:\n{csv_file}"
        )

    return csv_content


# ============================================================
# CALL CLAUDE
# ============================================================

def generate_claude_report(
    client: anthropic.Anthropic,
    report_name: str,
    prompt: str,
    csv_content: str,
) -> str:
    """
    Send ONE CSV to Claude using ONE report-specific prompt.
    """

    print(f"Calling Claude for: {report_name}")

    full_prompt = f"""
{prompt}

Report date: {REPORT_DATE}

Here is the CSV data:

```csv
{csv_content}
```
"""

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {
                "role": "user",
                "content": full_prompt,
            }
        ],
    )

    # Extract text from Claude's response.
    report_text = "\n".join(
        block.text
        for block in response.content
        if hasattr(block, "text")
    ).strip()

    if not report_text:
        raise RuntimeError(
            f"Claude returned an empty response for: "
            f"{report_name}"
        )

    return report_text


# ============================================================
# SAVE REPORT
# ============================================================

def save_report(
    report_name: str,
    report_text: str,
):
    """Save Claude's response as the matching TXT file."""

    output_file = OUTPUT_DIR / f"{report_name}.txt"

    output_file.write_text(
        report_text,
        encoding="utf-8",
    )

    print(f"Saved: {output_file}")


# ============================================================
# PROCESS ONE REPORT
# ============================================================

def process_report(
    client: anthropic.Anthropic,
    report_name: str,
    config: dict,
):
    """
    Process exactly one report:

        CSV
         ↓
       Prompt
         ↓
       Claude
         ↓
        TXT
    """

    print("----------------------------------------")
    print(f"Processing: {report_name}")

    # 1. Read the corresponding CSV
    csv_content = read_csv(report_name)

    # 2. Get this report's specific prompt
    prompt = config["prompt"]

    # 3. Send CSV + prompt to Claude
    report_text = generate_claude_report(
        client=client,
        report_name=report_name,
        prompt=prompt,
        csv_content=csv_content,
    )

    # 4. Save the response
    save_report(
        report_name=report_name,
        report_text=report_text,
    )

    print(f"Completed: {report_name}")


# ============================================================
# MAIN
# ============================================================

def main():

    print("========================================")
    print("Claude Daily Report Generator")
    print(f"Report date : {REPORT_DATE}")
    print(f"Output dir  : {OUTPUT_DIR}")
    print(f"Reports     : {len(REPORTS)}")
    print("========================================")

    # Validate environment
    validate_configuration()

    # Create Claude client
    client = anthropic.Anthropic(
        api_key=CLAUDE_API_KEY
    )

    # Process reports ONE BY ONE
    for report_name, config in REPORTS.items():

        process_report(
            client=client,
            report_name=report_name,
            config=config,
        )

    print("")
    print("========================================")
    print("All Claude reports generated successfully.")
    print("========================================")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
