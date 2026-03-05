# Confetti / Highfive

Confetti / Highfive is a lightweight Slack bot that keeps teams connected to each other's wins — the ones that slip by in the busy flow of the week.

Every Friday, it nudges your team to pause and reflect: not just what got done, but what's worth acknowledging. Shipping a feature, cracking a tough problem, getting through a hard week — big or small, saying it out loud matters.

Submissions take seconds. Pick a category, write a line, and choose to share publicly or anonymously. Public wins land in a shared channel; anonymous ones are logged privately with your team lead.

**What it does:**
- Automated Friday prompts via DM
- Clean submission modal — no friction
- Posts to a shared #small-wins channel
- Anonymous posting supported
- `/confetti` to share a win anytime (also `/highfive` or `/celebrate`)

Recognition shouldn't wait for the annual review — starting with recognising yourself.

## Features

- **Automated Friday prompts** - Sends a friendly DM to all members of a designated channel
- **Public or private sharing** - Users choose where their celebration goes
- **Category tagging** - Optional categories like "Project Milestone", "Learning", "Team Shoutout"
- **Interactive modals** - Clean Block Kit UI for entering celebrations
- **App Home tab** - Shows bot info and commands
- **Slash commands** - `/confetti` to share a win anytime (also `/highfive` or `/celebrate`)

## Quick Start

### 1. Create a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **Create New App** → **From scratch**
3. Name it "Celebrations Bot" and select your workspace

### 2. Configure Bot Permissions

Navigate to **OAuth & Permissions** and add these Bot Token Scopes:

```
channels:read        # Read channel membership
chat:write          # Send messages
commands            # Handle slash commands
users:read          # Check if users are bots
im:write            # Send DMs
```

### 3. Enable Features

**Interactivity & Shortcuts:**
- Turn ON Interactivity
- Set Request URL to: `https://your-domain.com/slack/events`

**Slash Commands** (create all three with the same Request URL):
- `/confetti` — "Share a win anytime" (primary)
- `/highfive` — alias
- `/celebrate` — alias
- Request URL: `https://your-domain.com/slack/events`

**App Home:**
- Enable Home Tab

**Event Subscriptions (if using HTTP mode):**
- Enable Events
- Request URL: `https://your-domain.com/slack/events`
- Subscribe to: `app_home_opened`

### 4. Install the App

1. Go to **Install App**
2. Click **Install to Workspace**
3. Copy the **Bot User OAuth Token** (starts with `xoxb-`)

### 5. Get Channel and User IDs

To find IDs in Slack:
- **Channel ID**: Right-click channel → View channel details → scroll to bottom
- **User ID**: Click on profile → More → Copy member ID

### 6. Set Environment Variables

```bash
export SLACK_BOT_TOKEN="xoxb-your-token"
export SLACK_SIGNING_SECRET="your-signing-secret"
export CELEBRATIONS_CHANNEL_ID="C01234ABCDE"
export PUBLIC_WINS_CHANNEL_ID="C01234ABCDE"
export ADMIN_USER_ID="U01234ABCDE"
export TIMEZONE="America/New_York"

# Optional: For Socket Mode (local development)
export SLACK_APP_TOKEN="xapp-your-app-token"
```

### 7. Install Dependencies

```bash
pip install -r requirements.txt
```

### 8. Run the Bot

**For development (Socket Mode):**
1. Enable Socket Mode in your Slack app settings
2. Generate an App-Level Token with `connections:write` scope
3. Run:
```bash
python app.py
```

**For production (HTTP mode):**
```bash
gunicorn app:app.server --bind 0.0.0.0:3000
```

## Scheduling Options

### Option 1: Cron Job

Add to your crontab (`crontab -e`):

```bash
# Run every Friday at 3 PM (server time)
0 15 * * 5 cd /path/to/bot && /path/to/python scheduler.py --send
```

### Option 2: Built-in Daemon

Run the scheduler as a background process:

```bash
python scheduler.py --daemon
```

### Option 3: AWS Lambda

1. Package the code:
```bash
pip install -r requirements.txt -t package/
cp *.py package/
cd package && zip -r ../deployment.zip .
```

2. Create Lambda function and upload `deployment.zip`

3. Set handler to: `scheduler.aws_lambda_handler`

4. Create CloudWatch Events rule:
```
cron(0 20 ? * FRI *)  # 3 PM EST = 8 PM UTC
```

### Option 4: Google Cloud Functions

```bash
gcloud functions deploy celebrations-bot \
  --runtime python311 \
  --trigger-http \
  --entry-point gcp_cloud_function \
  --set-env-vars SLACK_BOT_TOKEN=xoxb-...
```

Create a Cloud Scheduler job:
```bash
gcloud scheduler jobs create http celebrations-trigger \
  --schedule="0 15 * * 5" \
  --uri="YOUR_FUNCTION_URL" \
  --time-zone="America/New_York"
```

## Project Structure

```
slack-celebrations-bot/
├── app.py              # Main Slack Bolt application
├── config.py           # Configuration and settings
├── scheduler.py        # Scheduling logic
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Testing

**Send a test prompt immediately:**
```bash
python scheduler.py --send
```

**Check if current time matches schedule:**
```bash
python scheduler.py --check
```

**Test the slash command:**
Type `/confetti` (or `/highfive` / `/celebrate`) in any Slack channel

## Customization

Edit `config.py` to customize:
- `PROMPT_MESSAGE` - The Friday prompt text
- `SCHEDULE_DAY` - Day of week (0=Monday, 4=Friday)
- `SCHEDULE_HOUR` / `SCHEDULE_MINUTE` - Time of day
- `TIMEZONE` - Your timezone

## Message Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     Friday 3 PM                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Bot sends DM to each member of #celebrations channel       │
│  "Happy Friday! What's worth celebrating this week?"        │
│  [Share Publicly] [Share Privately] [Skip]                  │
└─────────────────────────────────────────────────────────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │  Public  │  │ Private  │  │   Skip   │
        └──────────┘  └──────────┘  └──────────┘
              │             │             │
              ▼             ▼             ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │  Modal   │  │  Modal   │  │ "See you │
        │  opens   │  │  opens   │  │  next    │
        └──────────┘  └──────────┘  │  week!"  │
              │             │       └──────────┘
              ▼             ▼
        ┌──────────┐  ┌──────────┐
        │ Posted   │  │ DM sent  │
        │ to #wins │  │ to admin │
        └──────────┘  └──────────┘
```

## Troubleshooting

**Bot not responding?**
- Check that all scopes are added and app is reinstalled
- Verify the signing secret matches
- Check logs for errors

**Not receiving DMs?**
- Make sure you're in the celebrations channel
- Check that the channel ID is correct
- Verify the bot has `im:write` scope

**Scheduler not running?**
- Check cron logs: `grep CRON /var/log/syslog`
- Verify environment variables are set for cron jobs
- Test with `python scheduler.py --send`

## License

MIT
