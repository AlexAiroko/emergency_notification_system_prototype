import pytest

from app.services.contact import ContactService


@pytest.fixture
def contact_service():
    return ContactService()
