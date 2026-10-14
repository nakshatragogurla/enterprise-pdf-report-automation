
import logging
import time
import schedule

from report_automation.main import main


def run_scheduler():
    """Run report generation on a scheduled basis."""
    logging.info("Report scheduler started.")

    schedule.every().day.at("09:00").do(main)

    print("Report scheduler started.")
    print("Reports will be generated daily at 9:00 AM.")
    print("Press Ctrl+C to stop.")

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        print("\nReport scheduler stopped.")
