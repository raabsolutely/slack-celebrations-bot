# Confetti / Highfive

Confetti / Highfive is a lightweight Slack bot that keeps teams connected to each other's wins — the ones that slip by in the busy flow of the week.

Every Friday, it nudges your team to pause and reflect: not just what got done, but what's worth acknowledging. Shipping a feature, cracking a tough problem, getting through a hard week — big or small, saying it out loud matters.

Submissions take seconds. Pick a category, write a line, and choose to share publicly or anonymously. Public wins land in a shared channel; anonymous ones are logged privately with your team lead.

**What it does:**
- Automated Friday prompts via DM to all members of a designated channel
- Clean submission modal — no friction
- Posts to a shared channel (e.g. #small-wins)
- Anonymous posting supported
- `/confetti` to share a win anytime (also `/highfive` or `/celebrate`)
- App Home tab with quick access buttons
- Opt-in / opt-out for Friday nudges

Recognition shouldn't wait for the annual review — starting with recognising yourself.

---

## Setup Guide

### 1. Clone the repo

```bash
git clone https://github.com/raabsolutely/slack-celebrations-bot.git
cd slack-celebrations-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create the Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **Create New App** → **From a manifest**
3. Select your workspace
4. Paste the contents of `slack-app-manifest.json`
5. Click **Next** → **Create**

This configures all scopes, slash commands, and features automatically.

### 4. Enable Socket Mode

1. In your app settings, go to **Socket Mode**
2. Toggle it **On**
3. Create an App-Level Token with the `connections:write` scope
4. Copy the token (starts with `xapp-`)

### 5. Install the app to your workspace

1. Go to **Install App** → **Install to Workspace** → **Allow**
2. Copy the **Bot User OAuth Token** (starts with `xoxb-`)
3. Copy the **Signing Secret** from **Basic Information**

### 6. Get channel and user IDs

To find IDs in Slack:
- **Channel ID**: Right-click channel → View channel details → scroll to bottom
- **User ID**: Click on a profile → More → Copy member ID

You'll need:
- `CELEBRATIONS_CHANNEL_ID` — the channel whose members receive the Friday DM prompt
- `SMALL_WINS_CHANNEL_ID` — the channel where public wins are posted
- `ADMIN_USER_ID` — the user who receives anonymous win notifications

### 7. Configure environment variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

```
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
SLACK_SIGNING_SECRET=...
CELEBRATIONS_CHANNEL_ID=C...
SMALL_WINS_CHANNEL_ID=C...
ADMIN_USER_ID=U...
TIMEZONE=Europe/Berlin
```

### 8. Run the bot

```bash
python run.py
```

The bot connects via Socket Mode — no public URL or firewall changes needed.

---

## Scheduling the Friday prompt

The bot DMs all members of `CELEBRATIONS_CHANNEL_ID` every Friday at 3 PM (configurable in `config.py`).

**Option 1 — Built-in daemon (recommended for always-on servers):**

Run `run.py` as a persistent service using systemd, supervisor, or your platform's process manager.

**Option 2 — Cron job:**

```bash
0 15 * * 5 cd /path/to/bot && python scheduler.py --send
```

**Test immediately (without waiting for Friday):**

```bash
python scheduler.py --send
```

---

## Project structure

```
slack-celebrations-bot/
├── app.py              # Slack Bolt app — event handlers, modals, slash commands
├── config.py           # All config: tokens, channel IDs, message templates
├── scheduler.py        # Friday 3 PM scheduling logic
├── run.py              # Entry point — validates config, starts bot
├── preferences.py      # Opt-in / opt-out persistence (user_prefs.json)
├── requirements.txt    # Python dependencies
├── .env.example        # Template for environment variables
└── slack-app-manifest.json  # Slack app config for one-click setup
```

---

## Test phase (beta rollout)

The recommended approach for testing before a full company rollout is a **private beta channel** — no code changes needed.

**How it works:**
1. Create a private Slack channel (e.g. `#confetti-beta`) and add only invited testers
2. Set `CELEBRATIONS_CHANNEL_ID` in `.env` to the ID of `#confetti-beta`
3. Friday DM prompts will go only to members of that channel — automatically scoped
4. Slash commands (`/confetti`, `/highfive`, `/celebrate`) are workspace-wide (this is an accepted tradeoff — non-testers finding the bot is fine)

**Full rollout:** swap `CELEBRATIONS_CHANNEL_ID` to the real target channel (e.g. `#general` or a dedicated `#confetti` channel). No code changes required.

---

## Customisation

Edit `config.py` to change:
- `PROMPT_MESSAGE` — the Friday prompt text
- `SCHEDULE_DAY` — day of week (0=Monday, 4=Friday)
- `SCHEDULE_HOUR` / `SCHEDULE_MINUTE` — time of day
- `TIMEZONE` — timezone for scheduling

---

## Troubleshooting

**Bot not responding to buttons or slash commands?**
- Make sure the bot is running (`python run.py`)
- Check that the app is installed to the workspace
- Verify Socket Mode is enabled and the App-Level Token is correct

**Not receiving Friday DMs?**
- Confirm you're a member of `CELEBRATIONS_CHANNEL_ID`
- Check that the channel ID in `.env` is correct
- Run `python scheduler.py --send` to test immediately

**Home tab spinning / not loading?**
- The bot must be running when the Home tab is opened
- Check that `app_home_opened` is subscribed under Event Subscriptions in app settings

**Multiple bot instances (stale behaviour):**
- Only one instance of `run.py` should be running at a time
- Check with: `ps aux | grep run.py`

---

## License

MIT
