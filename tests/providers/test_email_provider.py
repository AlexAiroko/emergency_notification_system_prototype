from unittest.mock import patch

import pytest

from app.providers.base import ProviderError
from app.providers.email import EmailProvider


def test_send_success():
    provider = EmailProvider()

    with patch("app.providers.email.smtplib.SMTP") as mock_smtp:
        smtp_instance = mock_smtp.return_value.__enter__.return_value

        message_id = provider.send(
            to="user@example.com",
            subject="Test Subject",
            body="Hello, world!",
        )

        mock_smtp.assert_called_once()
        smtp_instance.starttls.assert_called_once()
        smtp_instance.login.assert_called_once()
        smtp_instance.send_message.assert_called_once()

        sent_message = smtp_instance.send_message.call_args.args[0]

        assert sent_message["To"] == "user@example.com"
        assert sent_message["Subject"] == "Test Subject"
        assert sent_message["Message-ID"] is not None
        assert "Hello, world!" in sent_message.get_content()

        assert message_id == sent_message["Message-ID"]


def test_send_without_subject():
    provider = EmailProvider()

    with patch("app.providers.email.smtplib.SMTP") as mock_smtp:
        smtp_instance = mock_smtp.return_value.__enter__.return_value

        message_id = provider.send(
            to="user@example.com",
            body="Body only",
        )

        smtp_instance.send_message.assert_called_once()

        sent_message = smtp_instance.send_message.call_args.args[0]

        assert sent_message["To"] == "user@example.com"
        assert sent_message["Subject"] is None or sent_message["Subject"] == ""
        assert message_id is not None


@pytest.mark.parametrize(
    "smtp_method, error_message",
    [
        ("starttls", "TLS failed"),
        ("login", "Authentication failed"),
        ("send_message", "Send failed"),
    ],
)
def test_send_raises_provider_error(smtp_method, error_message):
    provider = EmailProvider()

    with patch("app.providers.email.smtplib.SMTP") as mock_smtp:
        smtp_instance = mock_smtp.return_value.__enter__.return_value

        getattr(smtp_instance, smtp_method).side_effect = Exception(error_message)

        with pytest.raises(ProviderError) as exc_info:
            provider.send(
                to="user@example.com",
                subject="Test",
                body="Hello",
            )

        assert error_message in str(exc_info.value)

        # optional: verify chaining (if implemented)
        assert isinstance(exc_info.value.__cause__, Exception)


def test_send_connection_error():
    provider = EmailProvider()

    with patch("app.providers.email.smtplib.SMTP") as mock_smtp:
        mock_smtp.side_effect = Exception("Connection failed")

        with pytest.raises(ProviderError) as exc_info:
            provider.send(
                to="user@example.com",
                subject="Test",
                body="Hello",
            )

        assert "Connection failed" in str(exc_info.value)
        assert isinstance(exc_info.value.__cause__, Exception)
