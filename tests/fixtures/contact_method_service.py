import pytest

from app.services.contact_method import ContactMethodService


@pytest.fixture
def contact_method_service():
    return ContactMethodService()
