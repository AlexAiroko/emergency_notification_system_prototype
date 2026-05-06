import pytest

from app.models.notification import Notification


@pytest.fixture
def notification(db_session, notification_template, group):
    obj = Notification(
        template_id=notification_template.id,
        group_id=group.id,
    )
    db_session.add(obj)
    db_session.flush()
    return obj
