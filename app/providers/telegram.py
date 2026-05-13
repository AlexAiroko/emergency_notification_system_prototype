import requests

from app.providers.base import BaseProvider, ProviderError


class TelegramProvider(BaseProvider):
    def __init__(self, token: str) -> None:
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}"
    
    def send(self, to: str, body: str, subject: str | None = None) -> str | None:
        url = f"{self.base_url}/sendMessage"

        payload = {
            "chat_id": to,
            "text": self._format_message(subject, body),
            "parse_mode": "HTML",
        }

        try:
            response = requests.post(url, json=payload, timeout=10) # type: ignore
            response.raise_for_status()

            data = response.json()

            if not data.get("ok"):
                raise ProviderError(f"Telegram API error: {data}")

            return str(data["result"]["message_id"])

        except Exception as exc:
            raise ProviderError(f"Telegram send failed: {exc}") from exc

    def _format_message(self, subject: str | None, body: str) -> str:
        if subject:
            return f"<b>{subject}</b>\n\n{body}"
        return body
