from unittest.mock import Mock

import pytest

from app.services.delivery import DeliveryService


@pytest.fixture
def delivery_service():
    service = DeliveryService(session=Mock())

    service.delivery_repo = Mock()
    service.notification_repo = Mock()
    service.template_service = Mock()

    return service
