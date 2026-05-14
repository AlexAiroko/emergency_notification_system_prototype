from app.models.contact import Contact
from app.repositories.group import GroupRepository


def test_create_group(db_session):
    repo = GroupRepository(db_session)

    group = repo.create(name="Admins")

    assert group.id is not None
    assert group.name == "Admins"


def test_get_group(db_session):
    repo = GroupRepository(db_session)

    created = repo.create(name="Team")

    found = repo.get(created.id)

    assert found is not None
    assert found.id == created.id
    assert found.name == "Team"


def test_get_group_not_found(db_session):
    repo = GroupRepository(db_session)

    result = repo.get(999999)

    assert result is None


def test_get_with_contacts_empty(db_session):
    repo = GroupRepository(db_session)

    group = repo.create(name="Empty Group")

    result = repo.get_with_contacts(group.id)

    assert result is not None
    assert result.contacts == []



def test_add_contact_to_group(db_session):
    group_repo = GroupRepository(db_session)

    group = group_repo.create(name="G1")

    contact = Contact(name="Alice")
    db_session.add(contact)
    db_session.flush()

    group_repo.add_contact(group.id, contact.id)
    db_session.flush()

    result = group_repo.get_with_contacts(group.id)

    assert len(result.contacts) == 1
    assert result.contacts[0].id == contact.id


def test_group_multiple_contacts(db_session):
    group_repo = GroupRepository(db_session)

    group = group_repo.create(name="G1")

    c1 = Contact(name="A")
    c2 = Contact(name="B")

    db_session.add_all([c1, c2])
    db_session.flush()

    group_repo.add_contact(group.id, c1.id)
    group_repo.add_contact(group.id, c2.id)
    db_session.flush()

    result = group_repo.get_with_contacts(group.id)

    ids = {c.id for c in result.contacts}

    assert ids == {c1.id, c2.id}


def test_remove_contact_from_group(db_session):
    group_repo = GroupRepository(db_session)

    group = group_repo.create(name="G1")

    contact = Contact(name="Alice")
    db_session.add(contact)
    db_session.flush()

    group_repo.add_contact(group.id, contact.id)
    db_session.flush()

    group_repo.remove_contact_from_group(group.id, contact.id)
    db_session.commit()

    result = group_repo.get_with_contacts(group.id)

    assert result.contacts == []


def test_remove_non_existing_contact_does_not_fail(db_session):
    repo = GroupRepository(db_session)

    group = repo.create(name="G1")

    repo.remove_contact_from_group(group.id, 999999)
    db_session.commit()

    result = repo.get(group.id)

    assert result is not None


def test_get_contacts_for_dispatch_empty(db_session):
    repo = GroupRepository(db_session)

    group = repo.create(name="G1")

    result = repo.get_contacts_for_dispatch(group.id)

    assert result == []


from app.models.contact_method import ContactMethod, ChannelType


def test_get_contacts_for_dispatch(db_session):
    repo = GroupRepository(db_session)

    group = repo.create(name="G1")

    contact = Contact(name="Bob")
    db_session.add(contact)
    db_session.flush()

    db_session.add(
        ContactMethod(
            contact_id=contact.id,
            channel=ChannelType.EMAIL,
            address="bob@mail.com",
        )
    )

    repo.add_contact(group.id, contact.id)
    db_session.flush()

    result = repo.get_contacts_for_dispatch(group.id)

    assert len(result) == 1
    assert result[0].id == contact.id
    assert len(result[0].contact_methods) == 1
