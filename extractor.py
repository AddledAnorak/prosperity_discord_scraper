import litellm

MODEL = "github_copilot/gemini-2.5-pro"

SYSTEM_PROMPT = """You are an expert trading analyst reviewing messages from a trading competition Discord channel.

Your job is to extract concrete, actionable trading strategies from the conversation. A good strategy includes one or more of:
- A specific entry/exit condition or signal
- A risk management rule (stop loss, position sizing, etc.)
- A market setup or pattern to watch for
- A specific instrument, timeframe, or indicator being used

Return ONLY a bullet-point list of distinct strategies found. If multiple people describe the same strategy, consolidate it into one bullet.
If there are no concrete strategies in the messages (just greetings, memes, off-topic chat), return exactly the string: NONE

Do not add explanations, preambles, or commentary. Just the bullet points or NONE."""


def extract_strategies(messages: list[dict]) -> str | None:
    """
    Analyze a batch of Discord messages and extract trading strategies.
    Returns a bullet-point string of strategies, or None if nothing found.
    """
    if not messages:
        return None

    # Format messages for the prompt
    conversation = "\n".join(
        f"[{m['author']['username']}]: {m['content']}"
        for m in messages
        if m.get("content")  # skip empty messages (attachments only, etc.)
    )

    if not conversation.strip():
        return None

    response = litellm.completion(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Here are the Discord messages:\n\n{conversation}"},
        ],
    )

    result = response.choices[0].message.content.strip()
    if result == "NONE" or not result:
        return None
    return result
