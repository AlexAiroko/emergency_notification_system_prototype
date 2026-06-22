from unittest.mock import Mock

import pytest

from app.services.delivery import DeliveryService


@pytest.fixture
def delivery_service():
    service = DeliveryService()
    service.template_service = Mock()
    return service
