"""Diagnose the contact form's Telegram notifications.

Checks the bot token, lists the chats the bot can reach, fills TELEGRAM_CHAT_ID
into .env when it is still empty, and sends a test message.

    python scripts/telegram_check.py
"""

import io
import json
import os
import re
from urllib import error as urllib_error
from urllib import request as urllib_request

from dotenv import load_dotenv

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(PROJECT_ROOT, ".env")


def call(token, method, payload=None):
    """Call one Telegram Bot API method. Returns the "result" field."""
    url = "https://api.telegram.org/bot%s/%s" % (token, method)
    data = json.dumps(payload).encode("utf-8") if payload else None
    headers = {"Content-Type": "application/json"} if payload else {}
    try:
        with urllib_request.urlopen(
            urllib_request.Request(url, data=data, headers=headers), timeout=10
        ) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib_error.HTTPError as error:
        body = json.loads(error.read().decode("utf-8", "replace") or "{}")
        raise SystemExit("FAIL %s -> HTTP %s: %s" % (
            method, error.code, body.get("description", body)))
    except urllib_error.URLError as error:
        raise SystemExit("FAIL %s -> no connection: %s" % (method, error.reason))
    return body["result"]


def save_chat_id(chat_id):
    """Write the chat id back into .env so the app picks it up on restart."""
    text = io.open(ENV_FILE, encoding="utf-8").read()
    text = re.sub(r"^TELEGRAM_CHAT_ID=.*$", "TELEGRAM_CHAT_ID=%s" % chat_id,
                  text, count=1, flags=re.MULTILINE)
    io.open(ENV_FILE, "w", encoding="utf-8", newline="\n").write(text)


def main():
    load_dotenv(ENV_FILE)
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token:
        raise SystemExit(
            "TELEGRAM_BOT_TOKEN is empty in .env.\n"
            "Open @BotFather in Telegram, send /newbot (or /mybots -> API Token),\n"
            "and paste the token into .env.")

    bot = call(token, "getMe")
    print("OK  token belongs to @%s" % bot["username"])

    # getUpdates only knows about chats that have messaged the bot - which is also
    # exactly the condition Telegram requires before the bot may write to them.
    chats = {}
    for update in call(token, "getUpdates"):
        chat = (update.get("message") or update.get("channel_post") or {}).get("chat")
        if chat:
            chats[chat["id"]] = chat.get("username") or chat.get("title") or chat.get("first_name", "")

    if not chat_id:
        if not chats:
            raise SystemExit(
                "TELEGRAM_CHAT_ID is empty and the bot has no messages yet.\n"
                "Open https://t.me/%s in Telegram, press Start, then run this again."
                % bot["username"])
        if len(chats) > 1:
            print("Several chats found - put one of these in TELEGRAM_CHAT_ID:")
            for found_id, name in chats.items():
                print("  %s  (%s)" % (found_id, name))
            return
        chat_id = str(next(iter(chats)))
        save_chat_id(chat_id)
        print("OK  TELEGRAM_CHAT_ID=%s written to .env" % chat_id)

    call(token, "sendMessage", {
        "chat_id": chat_id,
        "text": "Test message from your portfolio contact form.",
    })
    print("OK  test message sent to chat %s - check Telegram." % chat_id)


if __name__ == "__main__":
    main()
