from sqlalchemy import inspect

from app.models.contact_method import ChannelType, ContactMethod
from app.repositories.contact import ContactRepository


def test_create_contact(db_session):
    repo = ContactRepository(db_session)
    
    contact = repo.create(
        name="John Doe",
        external_id="ext-123",
    )
    
    assert contact.id is not None
    assert contact.name == "John Doe"
    assert contact.external_id == "ext-123"


def test_create_contact_with_null_external_id(db_session):
    repo = ContactRepository(db_session)

    contact = repo.create(name="NoExternal")

    assert contact.external_id is None
    
    db_session.expire_all()
    db_contact = repo.get(contact.id)

    assert db_contact.external_id is None
    assert db_contact.name == "NoExternal"
    


def test_create_persists_to_db(db_session):
    repo = ContactRepository(db_session)

    contact = repo.create(name="Persist")

    db_session.expire_all()

    loaded = repo.get(contact.id)

    assert loaded is not None
    assert loaded.name == "Persist"


def test_get_contact(db_session):
    repo = ContactRepository(db_session)
    
    created = repo.create(name="Alice")

    found = repo.get(created.id)
    
    assert found.id is not None
    assert found.id == created.id
    assert found.name == "Alice"


def test_get_contact_not_found(db_session):
    repo = ContactRepository(db_session)

    result = repo.get(999999)

    assert result is None


def test_get_many_order(db_session):
    repo = ContactRepository(db_session)

    repo.create(name="A")
    repo.create(name="B")
    repo.create(name="C")

    result = repo.get_many(limit=3)

    assert [c.name for c in result] == ["A", "B", "C"]


def test_get_many_empty(db_session):
    repo = ContactRepository(db_session)

    result = repo.get_many()

    assert result == []


def test_get_many_contacts_limit_no_offset(db_session):
    repo = ContactRepository(db_session)
    
    repo.create(name="User 1")
    repo.create(name="User 2")
    repo.create(name="User 3")
    
    contacts = repo.get_many(limit=2, offset=0)
    
    assert len(contacts) == 2
    assert contacts[0].name == "User 1"
    assert contacts[1].name == "User 2"


def test_get_many_contacts_limit_offset(db_session):
    repo = ContactRepository(db_session)
    
    repo.create(name="User 1")
    repo.create(name="User 2")
    repo.create(name="User 3")
    
    contacts = repo.get_many(limit=2, offset=1)
    
    assert len(contacts) == 2
    assert contacts[0].name == "User 2"
    assert contacts[1].name == "User 3"


def test_get_many_limit_zero(db_session):
    repo = ContactRepository(db_session)

    repo.create(name="A")
    repo.create(name="B")

    result = repo.get_many(limit=0)

    assert result == []


def test_get_many_offset_beyond_size(db_session):
    repo = ContactRepository(db_session)

    repo.create(name="A")
    repo.create(name="B")

    result = repo.get_many(limit=10, offset=100)

    assert result == []


def test_get_with_methods(db_session):
    repo = ContactRepository(db_session)
    
    contact = repo.create(name="Bob")
    
    db_session.add_all(
        [
            ContactMethod(
                contact_id=contact.id,
                channel=ChannelType.EMAIL,
                address="bob@example.com",
            ),
            ContactMethod(
                contact_id=contact.id,
                channel=ChannelType.SMS,
                address="+123456789",
            ),
        ]
    )
    
    db_session.flush()
    
    result = repo.get_with_methods(contact.id)
    
    assert result is not None
    assert result.id == contact.id
    assert len(result.contact_methods) == 2
    assert result.contact_methods[0].address in {
        "bob@example.com",
        "+123456789",
    }


def test_get_with_methods_not_found(db_session):
    repo = ContactRepository(db_session)

    result = repo.get_with_methods(999999)

    assert result is None


def test_get_with_methods_empty(db_session):
    repo = ContactRepository(db_session)

    contact = repo.create(name="Solo")

    result = repo.get_with_methods(contact.id)

    assert result is not None
    assert result.contact_methods == []


def test_get_with_methods_eager_loaded(db_session):
    repo = ContactRepository(db_session)

    contact = repo.create(name="Bob")

    db_session.add_all([
        ContactMethod(
            contact_id=contact.id,
            channel=ChannelType.EMAIL,
            address="a@a.com",
        )
    ])
    db_session.flush()
    db_session.expire_all()

    result = repo.get_with_methods(contact.id)

    # check that the relation is already loaded
    state = inspect(result)
    assert "contact_methods" not in state.unloaded


def test_contact_methods_belong_to_contact(db_session):
    repo = ContactRepository(db_session)

    contact = repo.create(name="Owner")

    db_session.add_all([
        ContactMethod(
            contact_id=contact.id,
            channel=ChannelType.EMAIL,
            address="owner@mail.com",
        ),
        ContactMethod(
            contact_id=contact.id,
            channel=ChannelType.SMS,
            address="+111",
        ),
    ])

    db_session.flush()

    result = repo.get_with_methods(contact.id)

    assert all(cm.contact_id == contact.id for cm in result.contact_methods)


def test_create_inactive_contact(db_session):
    repo = ContactRepository(db_session)

    contact = repo.create(
        name="Inactive",
        is_active=False,
    )

    assert contact.is_active is False

    db_session.expire_all()

    loaded = repo.get(contact.id)

    assert loaded.is_active is False


def test_get_active_contacts(db_session):
    repo = ContactRepository(db_session)

    repo.create(name="A")
    repo.create(name="B", is_active=False)
    repo.create(name="C")

    contacts = repo.get_active()

    assert len(contacts) == 2
    assert [c.name for c in contacts] == ["A", "C"]


def test_get_active_contacts_limit_offset(db_session):
    repo = ContactRepository(db_session)

    repo.create(name="A")
    repo.create(name="B", is_active=False)
    repo.create(name="C")
    repo.create(name="D")

    contacts = repo.get_active(
        limit=1,
        offset=1,
    )

    assert len(contacts) == 1
    assert contacts[0].name == "C"


def test_get_active_contacts_empty(db_session):
    repo = ContactRepository(db_session)

    repo.create(name="A", is_active=False)
    repo.create(name="B", is_active=False)

    contacts = repo.get_active()

    assert contacts == []


def test_update_contact(db_session):
    repo = ContactRepository(db_session)

    contact = repo.create(name="Old")

    repo.update(
        contact.id,
        "New",
    )

    db_session.expire_all()

    updated = repo.get(contact.id)

    assert updated.name == "New"


def test_update_not_existing_contact(db_session):
    repo = ContactRepository(db_session)

    repo.update(
        999999,
        "New",
    )

    assert repo.get(999999) is None


def test_activate_contact(db_session):
    repo = ContactRepository(db_session)

    contact = repo.create(
        name="User",
        is_active=False,
    )

    repo.activate(contact.id)

    db_session.expire_all()

    contact = repo.get(contact.id)

    assert contact.is_active is True


def test_deactivate_contact(db_session):
    repo = ContactRepository(db_session)

    contact = repo.create(name="User")

    repo.deactivate(contact.id)

    db_session.expire_all()

    contact = repo.get(contact.id)

    assert contact.is_active is False


def test_activate_then_deactivate_contact(db_session):
    repo = ContactRepository(db_session)

    contact = repo.create(
        name="User",
        is_active=False,
    )

    repo.activate(contact.id)

    db_session.expire_all()

    assert repo.get(contact.id).is_active is True

    repo.deactivate(contact.id)

    db_session.expire_all()

    assert repo.get(contact.id).is_active is False


def test_update_does_not_change_external_id(db_session):
    repo = ContactRepository(db_session)

    contact = repo.create(
        name="Old",
        external_id="ext-123",
    )

    repo.update(contact.id, "New")

    db_session.expire_all()

    updated = repo.get(contact.id)

    assert updated.name == "New"
    assert updated.external_id == "ext-123"
