import pytest

from app.models.contact import Contact
from app.models.contact_method import ChannelType, ContactMethod
from app.models.delivery import Delivery, DeliveryStatus
from app.repositories.delivery import DeliveryRepository


def test_create_delivery(db_session, notification, contact, contact_method):
    repo = DeliveryRepository(db_session)
    
    delivery = repo.create(
        notification_id=notification.id,
        contact_id=contact.id,
        contact_method_id=contact_method.id,
        channel="email",
        address="a@a.com",
    )

    assert delivery.id is not None
    assert delivery.status == DeliveryStatus.PENDING
    assert delivery.address == "a@a.com"


def test_create_bulk(db_session, notification, contact, contact_method, second_contact_with_method):
    repo = DeliveryRepository(db_session)

    contact2, contact_method2 = second_contact_with_method

    d1 = Delivery(
        notification_id=notification.id,
        contact_id=contact.id,
        contact_method_id=contact_method.id,
        channel="email",
        address="a@a.com",
    )

    d2 = Delivery(
        notification_id=notification.id,
        contact_id=contact2.id,
        contact_method_id=contact_method2.id,
        channel="sms",
        address="+111",
    )

    repo.create_bulk([d1, d2])
    db_session.flush()

    res = repo.get_by_notification(notification.id)

    assert len(res) == 2


@pytest.mark.parametrize("count", [0, 1, 5])
def test_get_by_notification(db_session, delivery_factory, notification, contact, contact_method, count):
    repo = DeliveryRepository(db_session)

    for _ in range(count):
        delivery_factory(
            notification_id=notification.id,
            contact_id=contact.id,
            contact_method_id=contact_method.id,
        )

    res = repo.get_by_notification(notification.id)

    assert len(res) == count


def test_update_status(db_session, delivery_factory, notification, contact, contact_method):
    repo = DeliveryRepository(db_session)

    delivery = delivery_factory(
        notification_id=notification.id,
        contact_id=contact.id,
        contact_method_id=contact_method.id,
    )

    repo.update_status(delivery.id, DeliveryStatus.SENT)
    db_session.flush()

    updated = repo.get_by_notification(notification.id)[0]

    assert updated.status == DeliveryStatus.SENT


@pytest.mark.parametrize("provider_id", [None, "msg-123"])
def test_mark_sent(db_session, delivery_factory, notification, contact, contact_method, provider_id):
    repo = DeliveryRepository(db_session)

    delivery = delivery_factory(
        notification_id=notification.id,
        contact_id=contact.id,
        contact_method_id=contact_method.id,
    )

    repo.mark_sent(delivery.id, provider_id)
    db_session.flush()

    updated = repo.get_by_notification(notification.id)[0]

    assert updated.status == DeliveryStatus.SENT
    assert updated.provider_message_id == provider_id


def test_mark_failed(db_session, delivery_factory, notification, contact, contact_method):
    repo = DeliveryRepository(db_session)

    delivery = delivery_factory(
        notification_id=notification.id,
        contact_id=contact.id,
        contact_method_id=contact_method.id,
    )

    repo.mark_failed(delivery.id, "network error")
    db_session.flush()

    updated = repo.get_by_notification(notification.id)[0]

    assert updated.status == DeliveryStatus.FAILED
    assert updated.error_message == "network error"


def test_get_stats(db_session, delivery_factory, notification, contact, contact_method, extra_contacts):
    repo = DeliveryRepository(db_session)

    c2, cm2 = extra_contacts[0]
    c3, cm3 = extra_contacts[1]

    delivery_factory(
        notification_id=notification.id,
        contact_id=contact.id,
        contact_method_id=contact_method.id,
        status=DeliveryStatus.SENT,
    )
    
    delivery_factory(
        notification_id=notification.id,
        contact_id=c2.id,
        contact_method_id=cm2.id,
        status=DeliveryStatus.SENT,
    )
    
    delivery_factory(
        notification_id=notification.id,
        contact_id=c3.id,
        contact_method_id=cm3.id,
        status=DeliveryStatus.FAILED,
    )

    stats = repo.get_stats(notification.id)

    assert stats["sent"] == 2
    assert stats["failed"] == 1
