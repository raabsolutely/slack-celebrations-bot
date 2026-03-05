"""
Configuration for the Slack Celebrations Bot
"""
import os

# =============================================================================
# SLACK CREDENTIALS (set via environment variables)
# =============================================================================
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")  # For Socket Mode (optional)

# =============================================================================
# CHANNEL CONFIGURATION
# =============================================================================
# The channel where subscribed users hang out - everyone here gets the Friday prompt
# Use the channel ID (e.g., "C01ABC123DE"), not the name
CELEBRATIONS_CHANNEL_ID = os.environ.get("CELEBRATIONS_CHANNEL_ID", "")

# The public channel where shared celebrations are posted (#small-wins)
SMALL_WINS_CHANNEL_ID = os.environ.get("SMALL_WINS_CHANNEL_ID", "")

# =============================================================================
# ADMIN CONFIGURATION
# =============================================================================
# User ID of the admin who receives private celebrations
# Use the user ID (e.g., "U01ABC123DE"), not the username
ADMIN_USER_ID = os.environ.get("ADMIN_USER_ID", "")

# =============================================================================
# SCHEDULING CONFIGURATION
# =============================================================================
# Day of week for the celebration prompt (0=Monday, 4=Friday)
SCHEDULE_DAY = 4  # Friday

# Hour to send the prompt (24-hour format)
SCHEDULE_HOUR = 15  # 3 PM

# Minute to send the prompt
SCHEDULE_MINUTE = 0

# Timezone for scheduling
TIMEZONE = os.environ.get("TIMEZONE", "America/New_York")

# =============================================================================
# MESSAGE TEMPLATES
# =============================================================================
PROMPT_MESSAGE = """
*Time to celebrate your wins or a team member.*

Take a moment to reflect: What's something worth celebrating? It could be:
• A project milestone you hit
• A problem you solved
• Something you learned
• A personal achievement

Share your win on the confetti channel!
"""

PUBLIC_CELEBRATION_HEADER = "*A Win Worth Celebrating!*"
PRIVATE_CELEBRATION_HEADER = ":lock: *Private Celebration Shared*"
