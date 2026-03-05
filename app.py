"""
Slack Celebrations Bot - Main Application

A Slack bot that prompts team members to share weekly wins and celebrations.
Users can choose to share publicly or privately with an admin.
"""
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError

from config import (
    SLACK_BOT_TOKEN,
    SLACK_SIGNING_SECRET,
    SLACK_APP_TOKEN,
    CELEBRATIONS_CHANNEL_ID,
    SMALL_WINS_CHANNEL_ID,
    ADMIN_USER_ID,
    PROMPT_MESSAGE,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Slack app
app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET,
)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_celebration_prompt_blocks():
    """
    Build the Block Kit blocks for the celebration prompt message.
    Includes buttons for sharing publicly or privately.
    """
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": PROMPT_MESSAGE
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Share a win",
                        "emoji": True
                    },
                    "style": "primary",
                    "action_id": "share_public",
                    "value": "public"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Skip This Week",
                        "emoji": True
                    },
                    "action_id": "skip_celebration"
                }
            ]
        }
    ]


def get_celebration_modal(share_type: str):
    """
    Build the modal view for entering a celebration.

    Args:
        share_type: Either 'public' or 'private'
    """
    title = "Share Your Win!" if share_type == "public" else "Private Win"
    submit_text = "Share with Team" if share_type == "public" else "Send to Admin"

    return {
        "type": "modal",
        "callback_id": f"celebration_submit_{share_type}",
        "title": {
            "type": "plain_text",
            "text": title
        },
        "submit": {
            "type": "plain_text",
            "text": submit_text
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel"
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*What's your celebration this week?*\n\nShare something you're proud of, grateful for, or excited about!"
                }
            },
            {
                "type": "input",
                "block_id": "celebration_input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "celebration_text",
                    "multiline": True,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "I'm celebrating..."
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": "Your Celebration"
                }
            },
            {
                "type": "input",
                "block_id": "category_input",
                "optional": True,
                "element": {
                    "type": "static_select",
                    "action_id": "category_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a category"
                    },
                    "options": [
                        {"text": {"type": "plain_text", "text": ":trophy: Project Milestone"}, "value": "milestone"},
                        {"text": {"type": "plain_text", "text": ":zap: Problem Solved"}, "value": "problem"},
                        {"text": {"type": "plain_text", "text": ":bulb: Today I Learned"}, "value": "learning"},
                        {"text": {"type": "plain_text", "text": ":star: Personal Win"}, "value": "personal"},
                        {"text": {"type": "plain_text", "text": ":sparkles: Other"}, "value": "other"}
                    ]
                },
                "label": {
                    "type": "plain_text",
                    "text": "Category"
                }
            },
            {
                "type": "input",
                "block_id": "anonymous_input",
                "optional": True,
                "element": {
                    "type": "checkboxes",
                    "action_id": "anonymous_check",
                    "options": [
                        {
                            "text": {"type": "plain_text", "text": "Post anonymously"},
                            "value": "anonymous"
                        }
                    ]
                },
                "label": {
                    "type": "plain_text",
                    "text": "Anonymity"
                }
            }
        ]
    }


def format_celebration_message(user_id: str, celebration_text: str, category: str = None, is_public: bool = True, anonymous: bool = False):
    """
    Format a celebration for posting to a channel or DM.
    """
    category_emoji = {
        "milestone": ":trophy:",
        "problem": ":zap:",
        "learning": ":bulb:",
        "personal": ":star:",
        "other": ":sparkles:"
    }

    attribution = "Shared by anonymous" if anonymous else f"Shared by <@{user_id}>"

    meta_parts = []
    if category:
        emoji = category_emoji.get(category, ":sparkles:")
        meta_parts.append(f"{emoji} {category.title()}")
    meta_parts.append(attribution)
    meta_text = "  ·  ".join(meta_parts)

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": celebration_text
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": meta_text
                }
            ]
        }
    ]

    return blocks


# =============================================================================
# SEND PROMPTS TO CHANNEL MEMBERS
# =============================================================================

def send_celebration_prompts():
    """
    Send celebration prompt DMs to all members of the celebrations channel.
    This function is called by the scheduler.
    """
    try:
        # Get channel members
        result = app.client.conversations_members(channel=CELEBRATIONS_CHANNEL_ID)
        members = result["members"]

        logger.info(f"Sending celebration prompts to {len(members)} channel members")

        blocks = get_celebration_prompt_blocks()
        success_count = 0

        for user_id in members:
            try:
                # Skip bots by checking user info
                user_info = app.client.users_info(user=user_id)
                if user_info["user"].get("is_bot", False):
                    continue

                # Send DM to user
                app.client.chat_postMessage(
                    channel=user_id,
                    text="Happy Friday! Time to share your weekly wins!",
                    blocks=blocks
                )
                success_count += 1
                logger.info(f"Sent prompt to user {user_id}")

            except SlackApiError as e:
                logger.error(f"Failed to send prompt to {user_id}: {e}")

        logger.info(f"Successfully sent {success_count} celebration prompts")
        return success_count

    except SlackApiError as e:
        logger.error(f"Error getting channel members: {e}")
        return 0


# =============================================================================
# BUTTON HANDLERS
# =============================================================================

@app.action("share_public")
def handle_share_public(ack, body, client):
    """Handle the 'Share Publicly' button click."""
    ack()

    try:
        client.views_open(
            trigger_id=body["trigger_id"],
            view=get_celebration_modal("public")
        )
    except SlackApiError as e:
        logger.error(f"Error opening public modal: {e}")


@app.action("share_private")
def handle_share_private(ack, body, client):
    """Handle the 'Share Privately' button click."""
    ack()

    try:
        client.views_open(
            trigger_id=body["trigger_id"],
            view=get_celebration_modal("private")
        )
    except SlackApiError as e:
        logger.error(f"Error opening private modal: {e}")


@app.action("skip_celebration")
def handle_skip(ack, body, client):
    """Handle the 'Skip This Week' button click."""
    ack()

    user_id = body["user"]["id"]

    try:
        client.chat_postMessage(
            channel=user_id,
            text="No problem! :slightly_smiling_face: We'll check in again next Friday. Have a great weekend!"
        )
    except SlackApiError as e:
        logger.error(f"Error sending skip confirmation: {e}")


# =============================================================================
# MODAL SUBMISSION HANDLERS
# =============================================================================

@app.view("celebration_submit_public")
def handle_public_submission(ack, body, client, view):
    """Handle public celebration modal submission."""
    ack()

    user_id = body["user"]["id"]

    # Extract values from the modal
    values = view["state"]["values"]
    celebration_text = values["celebration_input"]["celebration_text"]["value"]
    category = values["category_input"]["category_select"].get("selected_option")
    category_value = category["value"] if category else None
    anonymous_selected = values.get("anonymous_input", {}).get("anonymous_check", {}).get("selected_options", [])
    anonymous = len(anonymous_selected) > 0

    try:
        # Post to public channel
        blocks = format_celebration_message(user_id, celebration_text, category_value, is_public=True, anonymous=anonymous)

        client.chat_postMessage(
            channel=SMALL_WINS_CHANNEL_ID,
            text="Someone celebrates..." if anonymous else f"New celebration from <@{user_id}>!",
            blocks=blocks
        )

        # If anonymous, notify admin privately with the real identity
        if anonymous:
            client.chat_postMessage(
                channel=ADMIN_USER_ID,
                text=f":eye-in-speech-bubble: Anonymous celebration posted by <@{user_id}>:\n>{celebration_text}"
            )

        # Confirm to user via DM
        client.chat_postMessage(
            channel=user_id,
            text=":white_check_mark: Your celebration has been shared with the team! Thanks for spreading the positivity!"
        )

        logger.info(f"Public celebration posted by {user_id} (anonymous: {anonymous})")

    except Exception as e:
        logger.error(f"Error posting public celebration: {e}", exc_info=True)


@app.view("celebration_submit_private")
def handle_private_submission(ack, body, client, view):
    """Handle private celebration modal submission."""
    ack()

    user_id = body["user"]["id"]

    # Extract values from the modal
    values = view["state"]["values"]
    celebration_text = values["celebration_input"]["celebration_text"]["value"]
    category = values["category_input"]["category_select"].get("selected_option")
    category_value = category["value"] if category else None

    try:
        # Send to admin via DM
        blocks = format_celebration_message(user_id, celebration_text, category_value, is_public=False)

        client.chat_postMessage(
            channel=ADMIN_USER_ID,
            text=f"Private celebration from <@{user_id}>",
            blocks=blocks
        )

        # Confirm to user via DM
        client.chat_postMessage(
            channel=user_id,
            text=":white_check_mark: Your celebration has been shared privately with your team lead. Thanks for sharing! :star:"
        )

        logger.info(f"Private celebration sent by {user_id} to admin")

    except SlackApiError as e:
        logger.error(f"Error sending private celebration: {e}")


# =============================================================================
# SLASH COMMAND (OPTIONAL - for manual testing)
# =============================================================================

@app.command("/celebrate")
def handle_celebrate_command(ack, body, client):
    """Handle the /celebrate slash command — opens the share a win modal directly."""
    ack()

    try:
        client.views_open(
            trigger_id=body["trigger_id"],
            view=get_celebration_modal("public")
        )
    except SlackApiError as e:
        logger.error(f"Error opening modal from /celebrate: {e}")


# =============================================================================
# APP HOME BUTTON HANDLER
# =============================================================================

@app.action("home_share_win")
def handle_home_share_win(ack, body, client):
    """Handle the 'Share a Win' button on the App Home tab."""
    ack()

    try:
        client.views_open(
            trigger_id=body["trigger_id"],
            view=get_celebration_modal("public")
        )
    except SlackApiError as e:
        logger.error(f"Error opening modal from App Home: {e}")


# =============================================================================
# APP HOME TAB (OPTIONAL)
# =============================================================================

@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    """Update the App Home tab with info about the bot."""
    try:
        client.views_publish(
            user_id=event["user"],
            view={
                "type": "home",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*:tada: Welcome to Celebrations Bot!*"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Every Friday at 3 PM, I'll send you a reminder to share something worth celebrating from your week."
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*How it works:*\n\n1. :bell: Get a Friday prompt via DM\n2. :mega: Choose to share publicly or privately\n3. :star: Spread the positivity!"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Commands:*\n\n`/celebrate` - Share a win anytime!"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Share a Win",
                                    "emoji": True
                                },
                                "style": "primary",
                                "action_id": "home_share_win"
                            }
                        ]
                    }
                ]
            }
        )
    except Exception as e:
        logger.error(f"Error updating home tab: {e}")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # You can run in either Socket Mode (for development) or HTTP mode (for production)

    if SLACK_APP_TOKEN:
        # Socket Mode - great for local development
        logger.info("Starting app in Socket Mode...")
        handler = SocketModeHandler(app, SLACK_APP_TOKEN)
        handler.start()
    else:
        # HTTP Mode - use with a web server in production
        logger.info("Starting app in HTTP mode on port 3000...")
        app.start(port=3000)
