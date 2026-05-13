from unittest.mock import patch, Mock
import pytest

from app.providers.telegram import TelegramProvider
from app.providers.base import ProviderError


def test_telegram_send_success():
    provider = TelegramProvider(token="fake-token")

    mock_response = Mock()
    mock_response.json.return_value = {
        "ok": True,
        "result": {"message_id": 123},
    }
    mock_response.raise_for_status.return_value = None

    with patch("app.providers.telegram.requests.post", return_value=mock_response) as mock_post:
        message_id = provider.send(
            to="123456",
            subject="Hello",
            body="World",
        )

        assert message_id == "123"

        mock_post.assert_called_once()

        args, kwargs = mock_post.call_args
        assert "sendMessage" in args[0]

        payload = kwargs["json"]
        assert payload["chat_id"] == "123456"
        assert "<b>Hello</b>" in payload["text"]
        assert "World" in payload["text"]


def test_telegram_api_error():
    provider = TelegramProvider(token="fake-token")

    mock_response = Mock()
    mock_response.json.return_value = {
        "ok": False,
        "description": "Bad Request",
    }
    mock_response.raise_for_status.return_value = None

    with patch("app.providers.telegram.requests.post", return_value=mock_response):
        with pytest.raises(ProviderError) as exc_info:
            provider.send(
                to="123",
                body="Hello",
            )

        assert "Telegram API error" in str(exc_info.value)


def test_telegram_http_error():
    provider = TelegramProvider(token="fake-token")

    with patch("app.providers.telegram.requests.post") as mock_post:
        mock_post.side_effect = Exception("Connection failed")

        with pytest.raises(ProviderError) as exc_info:
            provider.send(
                to="123",
                body="Hello",
            )

        assert "Connection failed" in str(exc_info.value)


def test_telegram_without_subject():
    provider = TelegramProvider(token="fake-token")

    mock_response = Mock()
    mock_response.json.return_value = {
        "ok": True,
        "result": {"message_id": 10},
    }
    mock_response.raise_for_status.return_value = None

    with patch("app.providers.telegram.requests.post", return_value=mock_response):
        message_id = provider.send(
            to="123",
            body="Only body",
        )

        assert message_id == "10"
