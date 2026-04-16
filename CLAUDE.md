# Discord Trading Strategy Scraper

## Project Intent

This project monitors a Discord channel from an online trading competition and automatically extracts actionable trading strategies being discussed there. It runs as a periodic polling script — not a real-time bot — and saves extracted strategies to a Markdown file for review.

The owner only has regular member access to the Discord server (not admin), so it uses a **user token** against the Discord REST API directly. This is against Discord's Terms of Service; the owner is aware and accepts the risk.

---

## How It Works

1. **Poll**: Every N minutes (default: 15), fetch all new messages from the target channel using the Discord REST API with a user token.
2. **Track state**: `state.json` stores the ID of the last processed message so restarts never reprocess old messages.
3. **Extract**: New messages are batched and sent in a single call to Gemini via LiteLLM (authenticated through a GitHub Copilot subscription). The LLM is prompted to identify concrete trading strategies and ignore noise.
4. **Save**: Extracted strategies are appended as timestamped sections in `strategies.md`.

---

## File Overview

| File | Purpose |
|---|---|
| `scraper.py` | Entry point. Runs the polling loop using `schedule`. |
| `discord_client.py` | Hits the Discord REST API to fetch new messages. |
| `extractor.py` | Sends messages to Gemini via LiteLLM and extracts strategies. |
| `storage.py` | Appends extracted strategies to `strategies.md` with a UTC timestamp. |
| `requirements.txt` | Python dependencies. |
| `.env` | Secrets — **not committed**. See setup below. |
| `state.json` | Runtime state (last processed message ID) — **not committed**. Auto-created. |
| `strategies.md` | Output file — **not committed**. Auto-created. |

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Create `.env`
```
DISCORD_USER_TOKEN=your_user_token_here
DISCORD_CHANNEL_ID=your_channel_id_here
POLL_INTERVAL_MINUTES=15
```

- **DISCORD_USER_TOKEN**: Your Discord user token. Get it from the browser:  
  DevTools → Network tab → any Discord API request → copy the `Authorization` header value.
- **DISCORD_CHANNEL_ID**: Right-click the channel in Discord → "Copy Channel ID". Requires Developer Mode (Settings → Advanced → Developer Mode).

### 3. Run
```bash
python scraper.py
```

On **first run**, LiteLLM will prompt for GitHub Copilot OAuth (device flow). Open the printed URL in a browser, authorize once, and LiteLLM caches the token in `copilot_tokens/` for all future runs.

---

## LLM Configuration

- **Library**: `litellm`
- **Provider**: GitHub Copilot (authenticated via OAuth device flow on first use — no API key needed in `.env`)
- **Model**: `github_copilot/gemini-2.5-pro` (configured in `extractor.py:7`)  
  Change to `github_copilot/gemini-3-pro-preview` if that model is available in your Copilot plan.

---

## Current State (as of 2026-04-16)

- All core files implemented and working end-to-end.
- Repo pushed to `https://github.com/AddledAnorak/prosperity_discord_scraper`.
- The script has **not yet been run against a live channel** — you will need to fill in `.env` with real credentials first.
- No tests exist yet.
