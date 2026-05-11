import pytest

from app.repositories.notification_template import NotificationTemplateRepository


def test_create_template(db_session):
    repo = NotificationTemplateRepository(db_session)

    template = repo.create(
        name="Welcome",
        subject="Hello",
        body="Welcome to the system",
    )

    assert template.id is not None
    assert template.name == "Welcome"
    assert template.subject == "Hello"
    assert template.body == "Welcome to the system"
    assert template.is_active is True


def test_create_template_with_defaults(db_session):
    repo = NotificationTemplateRepository(db_session)

    template = repo.create(name="Only name", body="Only body")

    assert template.name == "Only name"
    assert template.subject is None
    assert template.body == "Only body"
    assert template.is_active is True


def test_get_template(db_session, notification_template):
    repo = NotificationTemplateRepository(db_session)

    found = repo.get(notification_template.id)

    assert found is not None
    assert found.id == notification_template.id
    assert found.body == notification_template.body


def test_get_template_not_found(db_session):
    repo = NotificationTemplateRepository(db_session)

    result = repo.get(999999)

    assert result is None


@pytest.mark.parametrize(
    "statuses, expected_count",
    [
        ([True], 1),
        ([True, False, True], 2),
        ([False, False], 0),
        ([], 0),
    ],
)
def test_get_active(db_session, statuses, expected_count):
    repo = NotificationTemplateRepository(db_session)

    for index, is_active in enumerate(statuses, start=1):
        repo.create(
            name=f"Template {index}",
            subject=f"Subject {index}",
            body=f"Body {index}",
            is_active=is_active,
        )

    templates = repo.get_active()

    assert len(templates) == expected_count
    assert all(template.is_active for template in templates)


def test_get_active_with_limit_and_offset(db_session):
    repo = NotificationTemplateRepository(db_session)

    repo.create(name="Name 1", body="Body 1", is_active=True)
    repo.create(name="Name 2", body="Body 2", is_active=True)
    repo.create(name="Name 3", body="Body 3", is_active=True)

    templates = repo.get_active(limit=2, offset=1)

    assert len(templates) == 2
    assert [template.name for template in templates] == [
        "Name 2",
        "Name 3",
    ]
    assert [template.body for template in templates] == [
        "Body 2",
        "Body 3",
    ]


def test_get_many(db_session):
    repo = NotificationTemplateRepository(db_session)

    repo.create(name="Name 1", body="Body 1")
    repo.create(name="Name 2", body="Body 2")
    repo.create(name="Name 3", body="Body 3")

    templates = repo.get_many(limit=2, offset=1)

    assert len(templates) == 2
    assert [template.name for template in templates] == [
        "Name 2",
        "Name 3",
    ]
    assert [template.body for template in templates] == [
        "Body 2",
        "Body 3",
    ]


def test_get_many_empty(db_session):
    repo = NotificationTemplateRepository(db_session)

    templates = repo.get_many()

    assert templates == []


def test_update_content(db_session, notification_template):
    repo = NotificationTemplateRepository(db_session)

    repo.update_content(
        notification_template.id,
        subject="Updated subject",
        body="Updated body",
    )
    db_session.flush()

    updated = repo.get(notification_template.id)

    assert updated.subject == "Updated subject"
    assert updated.body == "Updated body"


def test_deactivate_template(db_session, notification_template):
    repo = NotificationTemplateRepository(db_session)

    repo.deactivate(notification_template.id)
    db_session.flush()

    updated = repo.get(notification_template.id)

    assert updated.is_active is False


def test_activate_template(db_session, notification_template):
    repo = NotificationTemplateRepository(db_session)

    repo.deactivate(notification_template.id)
    db_session.flush()

    repo.activate(notification_template.id)
    db_session.flush()

    updated = repo.get(notification_template.id)

    assert updated.is_active is True


@pytest.mark.parametrize(
    "method_name, expected_state",
    [
        ("activate", True),
        ("deactivate", False),
    ],
)
def test_activation_methods(
    db_session,
    notification_template,
    method_name,
    expected_state,
):
    repo = NotificationTemplateRepository(db_session)

    getattr(repo, method_name)(notification_template.id)
    db_session.flush()

    updated = repo.get(notification_template.id)

    assert updated.is_active is expected_state


def test_activate_non_existing_template(db_session):
    repo = NotificationTemplateRepository(db_session)

    repo.activate(999999)
    db_session.flush()

    assert True


def test_deactivate_non_existing_template(db_session):
    repo = NotificationTemplateRepository(db_session)

    repo.deactivate(999999)
    db_session.flush()

    assert True
