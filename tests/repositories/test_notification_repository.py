from app.models.group import Group
from app.models.notification import NotificationStatus
from app.repositories.notification import NotificationRepository
from app.models.notification_template import NotificationTemplate


def test_create_notification(db_session, notification_template, group):
    repo = NotificationRepository(db_session)

    notification = repo.create(
        template_id=notification_template.id,
        group_id=group.id,
    )

    assert notification.id is not None
    assert notification.template_id == notification_template.id
    assert notification.group_id == group.id
    assert notification.status == NotificationStatus.PENDING


def test_get_notification(db_session, notification_template, group):
    repo = NotificationRepository(db_session)

    created = repo.create(notification_template.id, group.id)

    found = repo.get(created.id)

    assert found is not None
    assert found.id == created.id
    assert found.template_id == notification_template.id


def test_get_notification_not_found(db_session):
    repo = NotificationRepository(db_session)

    result = repo.get(999999)

    assert result is None


def test_get_with_relations(db_session, notification_template, group):
    repo = NotificationRepository(db_session)

    notification = repo.create(notification_template.id, group.id)

    result = repo.get_with_relations(notification.id)

    assert result is not None
    assert result.template is not None
    assert result.group is not None
    assert result.template.id == notification_template.id
    assert result.group.id == group.id


def test_get_with_relations_not_found(db_session):
    repo = NotificationRepository(db_session)

    result = repo.get_with_relations(999999)

    assert result is None


def test_mark_started(db_session, notification_template, group):
    repo = NotificationRepository(db_session)

    notification = repo.create(notification_template.id, group.id)

    repo.mark_started(notification.id)
    db_session.commit()

    updated = repo.get(notification.id)

    assert updated.status == NotificationStatus.IN_PROGRESS


def test_mark_started_without_commit(db_session, notification_template, group):
    repo = NotificationRepository(db_session)

    notification = repo.create(notification_template.id, group.id)

    repo.mark_started(notification.id)

    updated = repo.get(notification.id)
    assert updated.status == NotificationStatus.IN_PROGRESS


def test_mark_finished(db_session, notification_template, group):
    repo = NotificationRepository(db_session)

    notification = repo.create(notification_template.id, group.id)

    repo.mark_finished(notification.id)
    db_session.commit()

    updated = repo.get(notification.id)

    assert updated.status == NotificationStatus.SUCCESS


def test_update_status_direct(db_session, notification_template, group):
    repo = NotificationRepository(db_session)

    notification = repo.create(notification_template.id, group.id)

    repo.update_status(notification.id, NotificationStatus.SUCCESS)
    db_session.commit()

    updated = repo.get(notification.id)

    assert updated.status == NotificationStatus.SUCCESS


def test_update_status_non_existing(db_session):
    repo = NotificationRepository(db_session)

    repo.mark_started(999999)
    db_session.commit()

    # test should not fall
    assert True
