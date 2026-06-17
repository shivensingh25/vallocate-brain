# import subprocess
# import time
# from datetime import datetime
# import schedule


# def run_script(name):
#     """Run an ingestion script and print the result."""
#     print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Running {name}...")
#     try:
#         result = subprocess.run(
#             ["python", name],
#             capture_output=True,
#             text=True,
#             timeout=300,  # 5 minute timeout per script
#         )
#         if result.returncode == 0:
#             # Print last 3 lines of output (the summary)
#             lines = result.stdout.strip().split("\n")
#             for line in lines[-3:]:
#                 print(f"  {line}")
#         else:
#             print(f"  Error: {result.stderr[:200]}")
#     except subprocess.TimeoutExpired:
#         print(f"  Timeout: {name} took longer than 5 minutes")
#     except Exception as e:
#         print(f"  Failed: {e}")


# def run_all():
#     """Run all connectors."""
#     print(f"\n{'='*50}")
#     print(f"Full ingestion cycle starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#     print(f"{'='*50}")
#     run_script("company_brain.py")      # Google Chat
#     run_script("hubspot_ingest.py")     # HubSpot
#     run_script("gmail_ingest.py")       # Gmail
#     run_script("meeting_notes_ingest.py")  # Meeting Notes
#     run_script("clockify_ingest.py")    # Clockify
#     print(f"\n{'='*50}")
#     print(f"All connectors finished at {datetime.now().strftime('%H:%M:%S')}")
#     print(f"{'='*50}")


# # Schedule the runs
# schedule.every(6).hours.do(run_all)

# # Run immediately on startup, then follow schedule
# print("Vallocate Brain - Automated Scheduler")
# print("Running all connectors every 6 hours.")
# print("Press Ctrl+C to stop.\n")

# run_all()  # First run immediately

# while True:
#     schedule.run_pending()
#     time.sleep(60)  # Check every minute

import subprocess
import time
from datetime import datetime
import schedule


def run_script(name):
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Running {name}...")
    try:
        result = subprocess.run(
            ["python", name],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            for line in lines[-3:]:
                print(f"  {line}")
        else:
            print(f"  Error: {result.stderr[:200]}")
    except subprocess.TimeoutExpired:
        print(f"  Timeout: {name} took longer than 5 minutes")
    except Exception as e:
        print(f"  Failed: {e}")


def run_all():
    print(f"\n{'='*50}")
    print(f"Full ingestion cycle starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    run_script("company_brain.py")
    run_script("hubspot_ingest.py")
    run_script("gmail_ingest.py")
    run_script("meeting_notes_ingest.py")
    run_script("clockify_ingest.py")
    run_script("synthesize.py")
    print(f"\n{'='*50}")
    print(f"All connectors finished at {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*50}")


schedule.every(6).hours.do(run_all)

print("Vallocate Brain - Automated Scheduler")
print("Running all connectors every 6 hours.")
print("Press Ctrl+C to stop.\n")

run_all()

while True:
    schedule.run_pending()
    time.sleep(60)
