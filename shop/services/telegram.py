import json
import urllib.error
import urllib.request

from django.conf import settings


def send_order_to_telegram(text: str) -> bool:
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", "") or ""
    chat_id = getattr(settings, "TELEGRAM_CHAT_ID", "") or ""
    if not token or not chat_id:
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:  # noqa: S310
            return 200 <= resp.status < 300
    except (urllib.error.URLError, TimeoutError):
        return False
