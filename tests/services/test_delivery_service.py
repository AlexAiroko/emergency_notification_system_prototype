from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.models.contact_method import ChannelType
from app.models.delivery import DeliveryStatus
from app.providers.base import ProviderError


def test_send_success(delivery_service, uow):
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
    provider.send.return_value = "msg-123"

    uow.delivery_repo.get.return_value = delivery
    uow.notification_repo.get_with_relations.return_value = notification

    delivery_service.template_service.ensure_template_is_active = Mock(
        return_value=template,
    )

    delivery_service.provider_registry.get = Mock(
        return_value=provider,
    )

    delivery_service.send(uow, 1)

    delivery_service.template_service.ensure_template_is_active.assert_called_once_with(
        uow,
        100,
    )

    provider.send.assert_called_once_with(
        to="user@mail.com",
        subject="Subject",
        body="Body",
    )

    uow.delivery_repo.mark_sent.assert_called_once_with(
        1,
        provider_message_id="msg-123",
    )

    uow.delivery_repo.mark_failed.assert_not_called()


def test_send_delivery_not_found(delivery_service, uow):
    uow.delivery_repo.get.return_value = None

    with pytest.raises(
        ValueError,
        match="Delivery 1 not found",
    ):
        delivery_service.send(uow, 1)

    uow.notification_repo.get_with_relations.assert_not_called()


def test_send_notification_not_found(delivery_service, uow):
    delivery = SimpleNamespace(
        id=1,
        notification_id=10,
    )

    uow.delivery_repo.get.return_value = delivery
    uow.notification_repo.get_with_relations.return_value = None

    with pytest.raises(
        ValueError,
        match="Notification 10 not found",
    ):
        delivery_service.send(uow, 1)


def test_send_provider_error(delivery_service, uow):
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

    uow.delivery_repo.get.return_value = delivery
    uow.notification_repo.get_with_relations.return_value = notification

    delivery_service.template_service.ensure_template_is_active = Mock(
        return_value=template,
    )

    delivery_service.provider_registry.get = Mock(
        return_value=provider,
    )

    delivery_service.send(uow, 1)

    uow.delivery_repo.mark_failed.assert_called_once_with(
        1,
        error_message="SMTP failed",
    )

    uow.delivery_repo.mark_sent.assert_not_called()


def test_send_pending(delivery_service, uow):
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

    uow.delivery_repo.get_by_notification.return_value = [
        d1,
        d2,
        d3,
    ]

    delivery_service.send = Mock()

    delivery_service.send_pending(uow, 10)

    delivery_service.send.assert_any_call(
        uow,
        1,
    )

    delivery_service.send.assert_any_call(
        uow,
        3,
    )

    assert delivery_service.send.call_count == 2
