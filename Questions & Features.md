# Questions & Features

## To Do

- [x] Test opt-in / opt-out flow end to end
- [x] Register `/confetti` and `/highfive` slash commands in Slack app settings
- [x] Update bot display name to Confetti / Highfive (Bot User + reinstall app)
- [x] Update nudge message design
- [ ] Hand off to IT team for company Slack deployment
- [x] Enable Home Tab in Slack app settings (App Home → Show Tabs)

---

## Feature ideas

### User-controlled nudge frequency
Let users set how often they want to be nudged by the bot (e.g. weekly, bi-weekly, monthly, or never). Currently opt-out is all-or-nothing — a frequency setting would be a softer middle ground.

---

## Open questions

### Channel naming & placement
Proposed: bot posts into the same channel as shoutouts. Could potentially rename that channel to **#confetti** or **#highfive** to be more inclusive of personal wins — the current name "shoutouts" implies recognising others, whereas the bot also encourages celebrating yourself.

---

## Decisions made

### Anonymous posting
- Triggered via checkbox in the celebration modal
- Public post shows "Someone celebrates..." (no name)
- Admin always receives a private DM revealing who posted
