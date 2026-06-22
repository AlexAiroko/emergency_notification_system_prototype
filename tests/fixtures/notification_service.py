from unittest.mock import Mock, patch

import pytest

from app.services.notification import NotificationService


@pytest.fixture
def notification_service():
    """
    Creates a NotificationService with mocked dependencies.
    """
    with (
        patch("app.services.notification.NotificationRepository"),
        patch("app.services.notification.GroupRepository"),
        patch("app.services.notification.DeliveryRepository"),
        patch("app.services.notification.DeliveryService"),
        patch("app.services.notification.NotificationTemplateService"),
    ):
        service = NotificationService(session=Mock())

        service.notification_repo = Mock()
        service.group_repo = Mock()
        service.delivery_repo = Mock()
        service.delivery_service = Mock()
        service.template_service = Mock()

        return service
