"""
Entry point for the Slack Celebrations Bot.
Loads environment variables from .env, validates config, and starts the bot in Socket Mode.
"""
import os
import sys
import logging

# Load .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed — env vars must be set manually
    pass

# Validate required environment variables
required_vars = [
    "SLACK_BOT_TOKEN",
    "SLACK_SIGNING_SECRET",
    "SLACK_APP_TOKEN",
    "CELEBRATIONS_CHANNEL_ID",
    "SMALL_WINS_CHANNEL_ID",
    "ADMIN_USER_ID",
]

missing = [v for v in required_vars if not os.environ.get(v)]
if missing:
    print(f"ERROR: Missing required environment variables: {', '.join(missing)}")
    print("Check your .env file.")
    sys.exit(1)

# Start the bot
from app import app
from slack_bolt.adapter.socket_mode import SocketModeHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting Celebrations Bot in Socket Mode...")
handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
handler.start()
