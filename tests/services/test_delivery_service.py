from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.models.delivery import DeliveryStatus
from app.models.contact_method import ChannelType
from app.providers.base import ProviderError
from app.providers.email import EmailProvider
from app.providers.telegram import TelegramProvider


def test_send_success(delivery_service):
    delivery = SimpleNamespace(
        id=1,
        notification_id=10,
        channel=ChannelType.EMAIL,
        address="user@mail.com",
    )

    template = SimpleNamespace(
        subject="Subject",
        body="Body",
    )

    notification = SimpleNamespace(
        template_id=100,
    )

    provider = Mock()
    provider.send.return_value = "msg-123"

    delivery_service.delivery_repo.get.return_value = delivery
    delivery_service.notification_repo.get_with_relations.return_value = notification
    delivery_service.template_service.ensure_template_is_active.return_value = template

    delivery_service.provider_registry.get = Mock(return_value=provider)

    delivery_service.send(1)

    provider.send.assert_called_once_with(
        to="user@mail.com",
        subject="Subject",
        body="Body",
    )

    delivery_service.delivery_repo.mark_sent.assert_called_once_with(
        1,
        provider_message_id="msg-123",
    )

    delivery_service.delivery_repo.mark_failed.assert_not_called()


def test_send_delivery_not_found(delivery_service):
    delivery_service.delivery_repo.get.return_value = None

    with pytest.raises(
        ValueError,
        match="Delivery 1 not found",
    ):
        delivery_service.send(1)

    delivery_service.notification_repo.get_with_relations.assert_not_called()


def test_send_notification_not_found(delivery_service):
    delivery = SimpleNamespace(
        id=1,
        notification_id=10,
    )

    delivery_service.delivery_repo.get.return_value = delivery
    delivery_service.notification_repo.get_with_relations.return_value = None

    with pytest.raises(
        ValueError,
        match="Notification 10 not found",
    ):
        delivery_service.send(1)

    delivery_service.template_service.ensure_template_is_active.assert_not_called()


def test_send_provider_error(delivery_service):
    delivery = SimpleNamespace(
        id=1,
        notification_id=10,
        channel=ChannelType.EMAIL,
        address="user@mail.com",
    )

    notification = SimpleNamespace(
        template_id=100,
    )

    template = SimpleNamespace(
        subject="Subject",
        body="Body",
    )

    provider = Mock()
    provider.send.side_effect = ProviderError("SMTP failed")

    delivery_service.delivery_repo.get.return_value = delivery
    delivery_service.notification_repo.get_with_relations.return_value = notification
    delivery_service.template_service.ensure_template_is_active.return_value = template

    delivery_service.provider_registry.get = Mock(return_value=provider)

    delivery_service.send(1)

    delivery_service.delivery_repo.mark_failed.assert_called_once_with(
        1,
        error_message="SMTP failed",
    )

    delivery_service.delivery_repo.mark_sent.assert_not_called()


def test_send_pending(delivery_service):
    d1 = SimpleNamespace(
        id=1,
        status=DeliveryStatus.PENDING,
    )

    d2 = SimpleNamespace(
        id=2,
        status=DeliveryStatus.SENT,
    )

    d3 = SimpleNamespace(
        id=3,
        status=DeliveryStatus.PENDING,
    )

    delivery_service.delivery_repo.get_by_notification.return_value = [
        d1,
        d2,
        d3,
    ]

    delivery_service.send = Mock()

    delivery_service.send_pending(10)

    delivery_service.send.assert_any_call(1)
    delivery_service.send.assert_any_call(3)

    assert delivery_service.send.call_count == 2


def test_get_email_provider(delivery_service):
    provider = delivery_service.provider_registry.get(
        ChannelType.EMAIL,
    )

    assert isinstance(
        provider,
        EmailProvider,
    )


def test_get_telegram_provider(delivery_service):
    provider = delivery_service.provider_registry.get(
        ChannelType.TELEGRAM,
    )

    assert isinstance(
        provider,
        TelegramProvider,
    )


def test_get_provider_unsupported_channel(delivery_service):
    fake_channel = Mock()
    fake_channel.name = "WHATSAPP"

    with pytest.raises(
        ValueError,
        match="Unsupported channel",
    ):
        delivery_service.provider_registry.get(fake_channel)
