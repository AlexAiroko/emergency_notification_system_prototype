from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

from app.models.contact_method import ChannelType
from app.models.delivery import DeliveryStatus
from app.models.notification import NotificationStatus


def test_create_notification(notification_service):
    notification = SimpleNamespace(id=1)
    notification_service.notification_repo.create.return_value = notification

    email_method = SimpleNamespace(
        id=10,
        channel=ChannelType.EMAIL,
        address="user@example.com",
    )
    telegram_method = SimpleNamespace(
        id=11,
        channel=ChannelType.TELEGRAM,
        address="123456789",
    )

    contact = SimpleNamespace(
        id=100,
        contact_methods=[email_method, telegram_method],
    )

    notification_service.group_repo.get_contacts_for_dispatch.return_value = [contact]

    result = notification_service.create_notification(
        template_id=5,
        group_id=7,
    )

    assert result is notification

    notification_service.template_service.ensure_template_is_active.assert_called_once_with(5)

    notification_service.notification_repo.create.assert_called_once_with(
        template_id=5,
        group_id=7,
    )

    notification_service.group_repo.get_contacts_for_dispatch.assert_called_once_with(7)

    notification_service.delivery_repo.create_bulk.assert_called_once()

    deliveries = notification_service.delivery_repo.create_bulk.call_args.args[0]

    assert len(deliveries) == 2

    # проверяем первую delivery
    d1 = deliveries[0]
    assert d1.notification_id == 1
    assert d1.contact_id == 100
    assert d1.contact_method_id == 10
    assert d1.channel == ChannelType.EMAIL
    assert d1.address == "user@example.com"
    assert d1.status == DeliveryStatus.PENDING

    # проверяем вторую delivery
    d2 = deliveries[1]
    assert d2.notification_id == 1
    assert d2.contact_id == 100
    assert d2.contact_method_id == 11
    assert d2.channel == ChannelType.TELEGRAM
    assert d2.address == "123456789"
    assert d2.status == DeliveryStatus.PENDING


def test_create_notification_without_contacts(notification_service):
    notification = SimpleNamespace(id=1)

    notification_service.notification_repo.create.return_value = notification
    notification_service.group_repo.get_contacts_for_dispatch.return_value = []

    result = notification_service.create_notification(
        template_id=1,
        group_id=1,
    )

    assert result is notification

    notification_service.delivery_repo.create_bulk.assert_not_called()


def test_create_notification_with_contact_without_methods(notification_service):
    notification = SimpleNamespace(id=1)

    notification_service.notification_repo.create.return_value = notification

    contact = SimpleNamespace(
        id=100,
        contact_methods=[],
    )

    notification_service.group_repo.get_contacts_for_dispatch.return_value = [contact]

    notification_service.create_notification(
        template_id=1,
        group_id=1,
    )

    notification_service.delivery_repo.create_bulk.assert_not_called()


def test_start_notification(notification_service):
    notification_service.start_notification(123)

    notification_service.notification_repo.mark_started.assert_called_once_with(123)


def test_send_notification(notification_service):
    with patch.object(notification_service, "finalize_notification") as finalize_mock:
        notification_service.send_notification(42)

        notification_service.notification_repo.mark_started.assert_called_once_with(42)
        notification_service.delivery_service.send_pending.assert_called_once_with(42)
        finalize_mock.assert_called_once_with(42)


@pytest.mark.parametrize(
    ("stats", "expected_status"),
    [
        ({"sent": 3}, NotificationStatus.SUCCESS),
        ({"failed": 3}, NotificationStatus.FAILED),
        ({"sent": 2, "failed": 1}, NotificationStatus.PARTIAL_SUCCESS),
        ({"sent": 1, "failed": 1}, NotificationStatus.PARTIAL_SUCCESS),
    ],
)
def test_finalize_notification(notification_service, stats, expected_status):
    notification_service.delivery_repo.get_stats.return_value = stats

    notification_service.finalize_notification(1)

    notification_service.delivery_repo.get_stats.assert_called_once_with(1)

    notification_service.notification_repo.update_status.assert_called_once_with(
        1,
        expected_status,
    )


def test_finalize_notification_no_deliveries(notification_service):
    notification_service.delivery_repo.get_stats.return_value = {}

    notification_service.finalize_notification(1)

    notification_service.delivery_repo.get_stats.assert_called_once_with(1)
    notification_service.notification_repo.update_status.assert_not_called()


def test_create_notification_propagates_template_validation_error(notification_service):
    notification_service.template_service.ensure_template_is_active.side_effect = ValueError(
        "Template is inactive"
    )

    with pytest.raises(ValueError, match="Template is inactive"):
        notification_service.create_notification(
            template_id=1,
            group_id=1,
        )

    notification_service.notification_repo.create.assert_not_called()
    notification_service.group_repo.get_contacts_for_dispatch.assert_not_called()
    notification_service.delivery_repo.create_bulk.assert_not_called()
