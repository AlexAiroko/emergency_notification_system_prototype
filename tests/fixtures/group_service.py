import pytest

from app.services.group import GroupService


@pytest.fixture
def group_service():
    return GroupService()
