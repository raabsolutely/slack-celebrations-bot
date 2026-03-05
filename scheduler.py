"""
Scheduler for the Slack Celebrations Bot

This module handles the Friday 3 PM scheduling of celebration prompts.
It can be run as a standalone script via cron, or integrated with cloud schedulers.

Usage Options:
1. Cron job: 0 15 * * 5 python scheduler.py --send
2. Cloud Functions: Import and call trigger_celebration_prompts()
3. Always-on: python scheduler.py --daemon (runs continuously with built-in scheduling)
"""
import argparse
import logging
from datetime import datetime
import pytz

from config import (
    SCHEDULE_DAY,
    SCHEDULE_HOUR,
    SCHEDULE_MINUTE,
    TIMEZONE,
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def is_scheduled_time() -> bool:
    """
    Check if current time matches the scheduled time.
    Returns True if it's Friday at 3 PM (or whatever is configured).
    """
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)

    return (
        now.weekday() == SCHEDULE_DAY and
        now.hour == SCHEDULE_HOUR and
        now.minute == SCHEDULE_MINUTE
    )


def trigger_celebration_prompts():
    """
    Trigger sending celebration prompts to all subscribed users.
    This is the main function to call from external schedulers.
    """
    logger.info("Triggering celebration prompts...")

    # Import here to avoid circular imports and allow standalone usage
    from app import send_celebration_prompts

    count = send_celebration_prompts()
    logger.info(f"Celebration prompts sent to {count} users")
    return count


def run_daemon():
    """
    Run as a daemon process that checks the schedule every minute.
    Useful for simple deployments without external cron.
    """
    import time

    logger.info(f"Starting scheduler daemon")
    logger.info(f"Scheduled for: {['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][SCHEDULE_DAY]} at {SCHEDULE_HOUR:02d}:{SCHEDULE_MINUTE:02d} {TIMEZONE}")

    last_triggered = None

    while True:
        tz = pytz.timezone(TIMEZONE)
        now = datetime.now(tz)

        # Check if we should trigger
        if is_scheduled_time():
            today = now.date()
            if last_triggered != today:
                logger.info("Scheduled time reached, sending prompts...")
                trigger_celebration_prompts()
                last_triggered = today

        # Sleep for 30 seconds before checking again
        time.sleep(30)


def run_once():
    """
    Send prompts immediately (used by cron or manual trigger).
    """
    logger.info("Manual trigger - sending prompts now")
    count = trigger_celebration_prompts()
    print(f"Successfully sent celebration prompts to {count} users")


# =============================================================================
# CLOUD FUNCTION HANDLERS
# =============================================================================

def aws_lambda_handler(event, context):
    """
    AWS Lambda handler for scheduled events.

    Configure with CloudWatch Events rule:
    cron(0 15 ? * FRI *)  # Every Friday at 3 PM UTC (adjust for timezone)
    """
    logger.info(f"Lambda triggered with event: {event}")
    count = trigger_celebration_prompts()
    return {
        'statusCode': 200,
        'body': f'Sent celebration prompts to {count} users'
    }


def gcp_cloud_function(request):
    """
    Google Cloud Function handler.

    Configure with Cloud Scheduler:
    0 15 * * 5 (Every Friday at 3 PM)
    """
    logger.info("Cloud Function triggered")
    count = trigger_celebration_prompts()
    return f'Sent celebration prompts to {count} users', 200


def azure_function_handler(timer):
    """
    Azure Functions handler with timer trigger.

    Configure in function.json:
    "schedule": "0 0 15 * * 5"  # Every Friday at 3 PM
    """
    logger.info("Azure Function triggered")
    count = trigger_celebration_prompts()
    return count


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Slack Celebrations Bot Scheduler',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scheduler.py --send      Send prompts immediately
  python scheduler.py --daemon    Run as background scheduler
  python scheduler.py --check     Check if it's the scheduled time

For cron, add to crontab:
  0 15 * * 5 cd /path/to/bot && python scheduler.py --send
        """
    )

    parser.add_argument(
        '--send',
        action='store_true',
        help='Send celebration prompts immediately'
    )
    parser.add_argument(
        '--daemon',
        action='store_true',
        help='Run as a daemon process with built-in scheduling'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check if current time matches scheduled time (for testing)'
    )

    args = parser.parse_args()

    if args.send:
        run_once()
    elif args.daemon:
        run_daemon()
    elif args.check:
        tz = pytz.timezone(TIMEZONE)
        now = datetime.now(tz)
        scheduled = is_scheduled_time()
        print(f"Current time: {now.strftime('%A %H:%M')} {TIMEZONE}")
        print(f"Scheduled: {['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][SCHEDULE_DAY]} {SCHEDULE_HOUR:02d}:{SCHEDULE_MINUTE:02d}")
        print(f"Is scheduled time: {scheduled}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
