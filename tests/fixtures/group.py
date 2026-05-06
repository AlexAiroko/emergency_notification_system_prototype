import pytest

from app.models.group import Group


@pytest.fixture
def group(db_session):
    group = Group(name="G1")
    db_session.add(group)
    db_session.flush()
    return group
