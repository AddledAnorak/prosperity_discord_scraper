import os
from datetime import datetime, timezone

OUTPUT_FILE = "strategies.md"


def append_strategies(text: str) -> None:
    """Append extracted strategies with a UTC timestamp to strategies.md."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    section = f"\n## {timestamp}\n{text}\n"

    with open(OUTPUT_FILE, "a") as f:
        f.write(section)

    print(f"[storage] Wrote strategies to {OUTPUT_FILE}")
