# Confetti / Highfive — Project Memory

## What This Is
A Slack bot (formerly "Celebrations Bot", renamed to **Confetti / Highfive**) that automatically prompts users every Friday at 3pm (Europe/Berlin) to share a win from their week. Users respond via an interactive modal, and their celebration gets posted to a public channel.

## GitHub
https://github.com/raabsolutely/slack-celebrations-bot

## Local Project Path
`/Users/marcoraab/Claude local projects/slack-celebrations-bot`

## How to Run the Bot
Always kill existing instances first, then start fresh:
```bash
kill $(ps aux | grep "run.py" | grep -v grep | awk '{print $2}') 2>/dev/null
cd "/Users/marcoraab/Claude local projects/slack-celebrations-bot"
python3 run.py
```
> ⚠️ Not killing old instances causes multiple bots to run simultaneously, each serving stale code to Slack.

## Install Dependencies (if needed)
```bash
pip3 install slack-bolt slack-sdk pytz aiohttp python-dotenv
```

## File Structure
| File | Purpose |
|------|---------|
| `app.py` | Main Slack Bolt app — event handlers, modals, slash commands |
| `config.py` | All config: tokens, channel IDs, message templates |
| `scheduler.py` | Friday 3pm scheduling logic |
| `run.py` | Entry point — loads .env, validates config, starts bot |
| `requirements.txt` | Python dependencies |
| `.env` | Secret tokens (never commit this!) |
| `.env.example` | Template showing required env vars |
| `Questions & Features.md` | Open questions and design decisions log |

## Environment Variables (.env)
```
SLACK_BOT_TOKEN=xoxb-...        # Bot User OAuth Token
SLACK_APP_TOKEN=xapp-...        # App-Level Token (Socket Mode)
SLACK_SIGNING_SECRET=...        # Signing Secret
CELEBRATIONS_CHANNEL_ID=...     # Channel whose members get the Friday DM prompt
SMALL_WINS_CHANNEL_ID=...       # Channel where wins are posted (#small-wins)
ADMIN_USER_ID=...               # User ID of admin (receives anonymous win notifications)
TIMEZONE=Europe/Berlin
```

## Slack App Setup
- App lives at: https://api.slack.com/apps
- Uses **Socket Mode** (for local development — no public URL needed)
- Required bot scopes: `chat:write`, `commands`, `channels:read`, `users:read`, `im:write`
- Slash commands (register all three in Slack app settings):
  - `/confetti` — primary
  - `/highfive` — alias
  - `/celebrate` — alias
- To rename the bot in Slack: update **App Home → Bot User display name** AND reinstall the app

## UX Decisions Made
- ❌ Removed "share privately" button from Friday prompt
- ❌ Removed "a colleague helped you" bullet from prompt
- ❌ Removed "A Win Worth Celebrating!" header from posted messages
- ❌ Removed Team Shoutout category
- ✅ `/confetti` (and aliases) opens modal directly — no intermediate message
- ✅ "Share a Win" button on App Home tab
- ✅ Anonymous posting via checkbox — public post shows "Shared by anonymous", admin gets private DM with real identity
- ✅ Message layout: win text prominent, category + attribution on one metadata line
- ✅ Categories: 🏆 Project Milestone, ⚡ Problem Solved, 💡 Today I Learned, ⭐ Personal Win, ✨ Other
- ✅ Wins post to #small-wins (SMALL_WINS_CHANNEL_ID)

## Open To-Dos
> At the start of every session, show this list to the user before anything else.

- [ ] Hand off to IT team for company Slack deployment

*(Keep this list in sync with `Questions & Features.md`)*

## Current Status
- ✅ Bot fully working in personal test Slack workspace
- ✅ Code committed and pushed to GitHub
- ⏳ Company Slack deployment pending (needs IT team involvement)

## Pending Tasks
1. Test thoroughly in personal Slack
2. Hand off to company IT team for deployment
3. IT team needs to: create Slack app in company workspace, set up hosting, configure env vars

## IT Handoff Documents
- `Celebrations Bot - IT Brief.docx` — full setup guide for IT team
- `Celebrations Bot - IT Brief.pdf` — same, PDF version
- `README.md` — includes final app description for Slack Marketplace listing

## Known Issues & Fixes
- **Multiple bot instances**: Always kill all running instances before restarting. Use `ps aux | grep run.py` to check. Multiple instances cause stale code to be served.
- **Anonymous checkbox KeyError**: Fixed — use `.get()` chaining to safely read optional Slack block values.
- **Git index.lock**: If git fails with a lock file error, run `rm .git/index.lock`
- **Silent exit on `python3 run.py`**: Usually means `slack_bolt` isn't installed. Run `pip3 install slack-bolt slack-sdk pytz aiohttp python-dotenv`.
- **GitHub auth**: GitHub requires a Personal Access Token (not password) for push. Generate at github.com → Settings → Developer settings → Personal access tokens.
- **Bot name not updating in Slack**: Must update Bot User display name (not just Display Information) AND reinstall the app in the workspace.
