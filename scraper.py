import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import schedule
from dotenv import load_dotenv

import discord_client
import extractor
import storage

load_dotenv()

STATE_FILE = "state.json"
CHANNEL_ID = os.environ["DISCORD_CHANNEL_ID"]
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL_MINUTES", 15))


def load_state() -> dict:
    if Path(STATE_FILE).exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_message_id": None}


def save_state(state: dict) -> None:
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def poll() -> None:
    state = load_state()
    last_id = state.get("last_message_id")

    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')} UTC] Polling channel {CHANNEL_ID} "
          f"(after={last_id or 'beginning'}) ...")

    try:
        messages = discord_client.fetch_new_messages(CHANNEL_ID, last_id)
    except Exception as e:
        print(f"[error] Failed to fetch messages: {e}")
        return

    print(f"[poll] {len(messages)} new message(s) fetched.")

    if not messages:
        return

    # Update state with the newest message ID before processing,
    # so a crash during extraction doesn't reprocess the same messages.
    new_last_id = messages[-1]["id"]
    save_state({"last_message_id": new_last_id})

    try:
        strategies = extractor.extract_strategies(messages)
    except Exception as e:
        print(f"[error] LLM extraction failed: {e}")
        return

    if strategies:
        storage.append_strategies(strategies)
    else:
        print("[poll] No strategies found in this batch.")


def main() -> None:
    print(f"Discord Strategy Scraper started. Polling every {POLL_INTERVAL} minute(s).")
    print("Note: LiteLLM may prompt for GitHub Copilot OAuth on first run.\n")

    # Run immediately, then on schedule
    poll()
    schedule.every(POLL_INTERVAL).minutes.do(poll)

    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == "__main__":
    main()
