import pytest

from app.models.contact_method import ChannelType
from app.repositories.contact import ContactRepository
from app.repositories.contact_method import ContactMethodRepository


def test_create_contact_method(db_session, contact):
    repo = ContactMethodRepository(db_session)

    method = repo.create(
        contact_id=contact.id,
        channel=ChannelType.EMAIL,
        address="john@example.com",
    )

    assert method.id is not None
    assert method.contact_id == contact.id
    assert method.channel == ChannelType.EMAIL
    assert method.address == "john@example.com"


def test_get_contact_method(db_session, contact_method):
    repo = ContactMethodRepository(db_session)

    found = repo.get(contact_method.id)

    assert found is not None
    assert found.id == contact_method.id
    assert found.contact_id == contact_method.contact_id
    assert found.channel == contact_method.channel
    assert found.address == contact_method.address


def test_get_contact_method_not_found(db_session):
    repo = ContactMethodRepository(db_session)

    result = repo.get(999999)

    assert result is None


@pytest.mark.parametrize(
    "channels, expected_count",
    [
        ([ChannelType.EMAIL], 1),
        ([ChannelType.EMAIL, ChannelType.SMS], 2),
        ([ChannelType.EMAIL, ChannelType.SMS, ChannelType.TELEGRAM], 3),
        ([], 0),
    ],
)
def test_get_by_contact(db_session, contact, channels, expected_count):
    repo = ContactMethodRepository(db_session)

    for index, channel in enumerate(channels, start=1):
        repo.create(
            contact_id=contact.id,
            channel=channel,
            address=f"address-{index}",
        )

    methods = repo.get_by_contact(contact.id)

    assert len(methods) == expected_count
    assert [method.id for method in methods] == sorted(
        method.id for method in methods
    )


@pytest.mark.parametrize(
    "target_channel, expected_addresses",
    [
        (ChannelType.EMAIL, ["a@example.com", "b@example.com"]),
        (ChannelType.SMS, ["+111"]),
        (ChannelType.TELEGRAM, []),
    ],
)
def test_get_by_contact_and_channel(
    db_session,
    contact,
    target_channel,
    expected_addresses,
):
    repo = ContactMethodRepository(db_session)

    repo.create(
        contact_id=contact.id,
        channel=ChannelType.EMAIL,
        address="a@example.com",
    )
    repo.create(
        contact_id=contact.id,
        channel=ChannelType.EMAIL,
        address="b@example.com",
    )
    repo.create(
        contact_id=contact.id,
        channel=ChannelType.SMS,
        address="+111",
    )

    methods = repo.get_by_contact_and_channel(
        contact.id,
        target_channel,
    )

    assert [method.address for method in methods] == expected_addresses


def test_get_by_contact_does_not_return_other_contacts(
    db_session,
    contact,
):
    repo = ContactMethodRepository(db_session)

    repo.create(
        contact_id=contact.id,
        channel=ChannelType.EMAIL,
        address="owner@example.com",
    )

    other_contact = ContactRepository(db_session).create(name="Other")

    repo.create(
        contact_id=other_contact.id,
        channel=ChannelType.EMAIL,
        address="other@example.com",
    )

    methods = repo.get_by_contact(contact.id)

    assert len(methods) == 1
    assert methods[0].address == "owner@example.com"


def test_delete_contact_method(db_session, contact_method):
    repo = ContactMethodRepository(db_session)

    repo.delete(contact_method.id)
    db_session.flush()

    result = repo.get(contact_method.id)

    assert result is None


def test_delete_non_existing_contact_method(db_session):
    repo = ContactMethodRepository(db_session)

    # Method shouldn't throw an exception
    repo.delete(999999)
    db_session.flush()

    assert True
