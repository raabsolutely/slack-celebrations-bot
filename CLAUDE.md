# Slack Celebrations Bot — Project Memory

## What This Is
A Slack bot that automatically prompts users every Friday at 3pm (Europe/Berlin) to share a win from their week. Users respond via an interactive modal, and their celebration gets posted to a public channel.

## GitHub
https://github.com/raabsolutely/slack-celebrations-bot

## Local Project Path
`/Users/marcoraab/Claude local projects/slack-celebrations-bot`

> ⚠️ Do NOT work from the Dropbox copy — it causes file locking issues. Always use the local path above.

## How to Run the Bot
```bash
cd "/Users/marcoraab/Claude local projects/slack-celebrations-bot"
python3 run.py
```
The bot should print connection messages and connect via Socket Mode. If it exits silently, check that dependencies are installed.

## Install Dependencies (if needed)
```bash
pip3 install slack-bolt slack-sdk pytz aiohttp
```

## File Structure
| File | Purpose |
|------|---------|
| `app.py` | Main Slack Bolt app — event handlers, modals, /celebrate command |
| `config.py` | All config: tokens, channel IDs, message templates |
| `scheduler.py` | Friday 3pm scheduling logic |
| `run.py` | Entry point — loads .env, validates config, starts bot |
| `requirements.txt` | Python dependencies |
| `.env` | Secret tokens (never commit this!) |
| `.env.example` | Template showing required env vars |

## Environment Variables (.env)
```
SLACK_BOT_TOKEN=xoxb-...        # Bot User OAuth Token
SLACK_APP_TOKEN=xapp-...        # App-Level Token (Socket Mode)
SLACK_SIGNING_SECRET=...        # Signing Secret
CELEBRATIONS_CHANNEL_ID=...     # Channel where Friday prompts go out
SMALL_WINS_CHANNEL_ID=...       # Channel where wins get posted (#small-wins)
ADMIN_USER_ID=...               # User ID of admin (receives private wins)
TIMEZONE=Europe/Berlin
```

## Slack App Setup
- App lives at: https://api.slack.com/apps
- Uses **Socket Mode** (for local development — no public URL needed)
- Required bot scopes: `chat:write`, `commands`, `channels:read`, `users:read`
- Slash command: `/celebrate`

## UX Decisions Made So Far
- ❌ Removed "share privately" button
- ❌ Removed "a colleague helped you" bullet point from prompt
- ❌ Removed emojis from modal headers
- ✅ Button text is "Share a win"
- ✅ Wins post to #celebrations channel (PUBLIC_WINS_CHANNEL_ID)

## Current Status
- ✅ Bot fully working in personal test Slack workspace
- ✅ Code committed and pushed to GitHub
- ⏳ UX adjustments still pending before company deployment
- ⏳ Company Slack deployment pending (needs IT team involvement)

## Pending Tasks
1. Make any remaining UX changes to the bot
2. Test thoroughly in personal Slack
3. Hand off to company IT team for deployment
4. IT team needs to: create Slack app in company workspace, set up hosting, configure env vars

## IT Handoff Documents
- `Celebrations Bot - IT Brief.docx` — full setup guide for IT team
- `Celebrations Bot - IT Brief.pdf` — same, PDF version

## Known Issues & Fixes
- **Dropbox file locking**: Working from Dropbox causes `Resource deadlock` and `Operation timed out` errors. Solution: always work from the local copy at `~/Claude local projects/slack-celebrations-bot`.
- **Git index.lock**: If git fails with a lock file error, run `rm .git/index.lock`
- **Silent exit on `python3 run.py`**: Usually means `slack_bolt` isn't installed. Run `pip3 install slack-bolt slack-sdk pytz aiohttp`.
- **GitHub auth**: GitHub requires a Personal Access Token (not password) for push. Generate at github.com → Settings → Developer settings → Personal access tokens.
