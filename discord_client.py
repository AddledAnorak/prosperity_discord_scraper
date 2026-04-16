import os
import requests

DISCORD_API = "https://discord.com/api/v9"


def fetch_new_messages(channel_id: str, after_message_id: str | None) -> list[dict]:
    """
    Fetch messages from a Discord channel newer than after_message_id.
    Returns a list of message dicts sorted oldest-first.
    Uses a user token (no 'Bot' prefix).
    """
    token = os.environ["DISCORD_USER_TOKEN"]
    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    }
    params = {"limit": 100}
    if after_message_id:
        params["after"] = after_message_id

    url = f"{DISCORD_API}/channels/{channel_id}/messages"
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 401:
        raise ValueError("Discord returned 401 Unauthorized. Check your DISCORD_USER_TOKEN.")
    if response.status_code == 403:
        raise ValueError("Discord returned 403 Forbidden. You may not have access to this channel.")
    if response.status_code != 200:
        raise RuntimeError(f"Discord API error {response.status_code}: {response.text}")

    messages = response.json()
    # API returns newest-first; reverse to get oldest-first
    return list(reversed(messages))
