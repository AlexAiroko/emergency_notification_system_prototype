import logging
import requests

from app.providers.base import BaseProvider, ProviderError


logger = logging.getLogger(__name__)


class TelegramProvider(BaseProvider):
    def __init__(self, token: str) -> None:
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send(self, to: str, body: str, subject: str | None = None) -> str | None:
        url = f"{self.base_url}/sendMessage"

        logger.info(
            "Started sending telegram message (chat_id=%s)",
            to,
        )

        payload = {
            "chat_id": to,
            "text": self._format_message(subject, body),
            "parse_mode": "HTML",
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data.get("ok"):
                logger.warning(
                    "Telegram API returned not ok (chat_id=%s, response=%s)",
                    to,
                    data,
                )
                raise ProviderError(f"Telegram API error: {data}")

            message_id = str(data["result"]["message_id"])

            logger.info(
                "Telegram message sent successfully (chat_id=%s, message_id=%s)",
                to,
                message_id,
            )

            return message_id

        except requests.RequestException as exc:
            logger.exception(
                "Telegram request failed (chat_id=%s)",
                to,
            )
            raise ProviderError(f"Telegram send failed: {exc}") from exc

        except Exception as exc:
            logger.exception(
                "Unexpected error while sending telegram message (chat_id=%s)",
                to,
            )
            raise ProviderError(f"Telegram send failed: {exc}") from exc

    def _format_message(self, subject: str | None, body: str) -> str:
        if subject:
            return f"<b>{subject}</b>\n\n{body}"
        return body
