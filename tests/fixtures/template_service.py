from unittest.mock import Mock

import pytest

from app.services.notification_template import NotificationTemplateService


@pytest.fixture
def template_service():
    return NotificationTemplateService()
