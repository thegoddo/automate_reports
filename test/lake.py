import time
import pyautogui as pg
import pyperclip
import pywhatkit as pwk

# 1. Configuration
group_id = "BmXPTGGbTxt3yMv5L4VNtb"

# Your multi-line report (50-60 lines)
message = """📊 DAILY AUTOMATED REPORT
----------------------------------
Line 1: System status nominal.
Line 2: Data processing completed successfully.
... (Add your remaining 50-60 lines here) ...
Line 60: End of report.
"""

# 2. Copy the full report to the system clipboard
pyperclip.copy(message)

# 3. Open WhatsApp Web group using pywhatkit (passing a space so it doesn't type)
# Keep tab_close=False initially so it doesn't close before we paste
pwk.sendwhatmsg_to_group_instantly(group_id, " ", wait_time=15, tab_close=False)

# 4. Wait brief moment for chat input box focus, then Paste (Ctrl+V) & Send (Enter)
time.sleep(2)
pg.hotkey("ctrl", "v")  # Instantly pastes the 60-line report
time.sleep(1)
pg.press("enter")  # Sends the message

# 5. Optional: Close browser tab after sending
time.sleep(2)
pg.hotkey("ctrl", "w")
