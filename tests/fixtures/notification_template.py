import pytest

from app.models.notification_template import NotificationTemplate


@pytest.fixture
def notification_template(db_session):
    template = NotificationTemplate(
        name="T1",
        subject="Subj",
        body="Body text",
        is_active=True,
    )
    db_session.add(template)
    db_session.flush()
    return template
