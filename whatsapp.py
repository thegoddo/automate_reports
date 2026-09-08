#!/usr/bin/env python3

import json
import time
from datetime import date, timedelta
from pathlib import Path

import pyautogui as pg
import pyperclip
import pywhatkit as pwk


# ============================================================
# CONFIGURATION
# ============================================================

WAIT_TIME = 15
CLOSE_TAB = True


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

REPORT_DATE = (
    date.today() - timedelta(days=1)
).isoformat()

OUTPUT_DIR = BASE_DIR / "output" / REPORT_DATE

GROUP_CONFIG_FILE = (
    BASE_DIR / "config" / "whatsapp_groups.json"
)


# ============================================================
# LOAD GROUP CONFIGURATION
# ============================================================

PLACEHOLDER_VALUES = {
    "ANOTHER_GROUP_ID",
    "ISSUES_GROUP_ID",
    "COMPLIMENTS_GROUP_ID",
    "YOUR_GROUP_ID_1",
    "YOUR_GROUP_ID_2",
    "YOUR_GROUP_ID_3",
    "YOUR_GROUP_ID_4",
    "YOUR_GROUP_ID_5",
    "YOUR_GROUP_ID_6",
    "YOUR_GROUP_ID_7",
}

def load_group_config() -> dict:

    if not GROUP_CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"WhatsApp group configuration not found:\n"
            f"{GROUP_CONFIG_FILE}"
        )

    with GROUP_CONFIG_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


# ============================================================
# READ REPORT
# ============================================================

def read_report(report_name: str) -> str:

    report_file = (
        OUTPUT_DIR / f"{report_name}.txt"
    )

    if not report_file.exists():
        raise FileNotFoundError(
            f"Report file not found:\n{report_file}"
        )

    report = report_file.read_text(
        encoding="utf-8"
    ).strip()

    if not report:
        raise RuntimeError(
            f"Report file is empty:\n{report_file}"
        )

    return report


# ============================================================
# SEND REPORT
# ============================================================

def send_report(
    report_name: str,
    group_id: str,
):
    if group_id in PLACEHOLDER_VALUES:
        raise RuntimeError(
            f"WhatsApp group ID for '{report_name}' is not configured.\n"
            f"Current value: {group_id}\n"
            f"Please update whatsapp_groups.json with a real group ID."
        )

    print("----------------------------------------")
    print(f"Report : {report_name}")
    print(f"Group  : {group_id}")

    report = read_report(report_name)

    pyperclip.copy(report)

    print("Opening WhatsApp Web...")

    pwk.sendwhatmsg_to_group_instantly(
        group_id,
        " ",
        wait_time=WAIT_TIME,
        tab_close=False,
    )

    time.sleep(2)

    print("Pasting report...")

    pg.hotkey("ctrl", "v")

    time.sleep(1)

    print("Sending report...")

    pg.press("enter")

    time.sleep(2)

    if CLOSE_TAB:
        print("Closing WhatsApp Web tab...")
        pg.hotkey("ctrl", "w")

        time.sleep(1)

    print("Report sent successfully.")


# ============================================================
# MAIN
# ============================================================

def main():

    print("========================================")
    print("WhatsApp Daily Reports")
    print(f"Report date: {REPORT_DATE}")
    print("========================================")

    if not OUTPUT_DIR.exists():
        raise FileNotFoundError(
            f"Output directory does not exist:\n{OUTPUT_DIR}"
        )

    groups = load_group_config()

    for report_name, group_id in groups.items():

        if not group_id:
            raise RuntimeError(
                f"No group ID configured for {report_name}"
            )

        send_report(
            report_name,
            group_id,
        )

        # Small delay between reports
        time.sleep(3)

    print("")
    print("========================================")
    print("All WhatsApp reports sent.")
    print("========================================")


if __name__ == "__main__":
    main()
