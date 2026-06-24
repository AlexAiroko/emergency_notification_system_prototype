from types import SimpleNamespace

import pytest
from sqlalchemy.exc import IntegrityError

from app.exceptions.contact import ContactNotFoundError
from app.exceptions.group import (
    GroupAlreadyExistsError,
    GroupNotFoundError,
)


def test_create_group(group_service, uow):
    group = SimpleNamespace(id=1, name="Admins")

    uow.group_repo.create.return_value = group

    result = group_service.create_group(
        uow,
        name="Admins",
    )

    assert result is group

    uow.group_repo.create.assert_called_once_with(
        name="Admins",
    )


def test_create_group_already_exists(group_service, uow):
    uow.group_repo.create.side_effect = IntegrityError(
        statement="",
        params={},
        orig=Exception(),
    )

    with pytest.raises(GroupAlreadyExistsError):
        group_service.create_group(
            uow,
            name="Admins",
        )


def test_get_group(group_service, uow):
    group = SimpleNamespace(id=1)

    uow.group_repo.get.return_value = group

    result = group_service.get_group(
        uow,
        1,
    )

    assert result is group

    uow.group_repo.get.assert_called_once_with(1)


def test_get_group_not_found(group_service, uow):
    uow.group_repo.get.return_value = None

    with pytest.raises(
        GroupNotFoundError,
        match="Group 1 not found",
    ):
        group_service.get_group(
            uow,
            1,
        )


def test_get_many_groups(group_service, uow):
    groups = [
        SimpleNamespace(id=1),
        SimpleNamespace(id=2),
    ]

    uow.group_repo.get_many.return_value = groups

    result = group_service.get_many_groups(
        uow,
        limit=10,
        offset=5,
    )

    assert result == groups

    uow.group_repo.get_many.assert_called_once_with(
        limit=10,
        offset=5,
    )


def test_update_group(group_service, uow):
    uow.group_repo.get.return_value = SimpleNamespace(id=1)

    group_service.update_group(
        uow,
        group_id=1,
        name="Updated",
    )

    uow.group_repo.update.assert_called_once_with(
        obj_id=1,
        name="Updated",
    )


def test_update_group_not_found(group_service, uow):
    uow.group_repo.get.return_value = None

    with pytest.raises(
        GroupNotFoundError,
        match="Group 1 not found",
    ):
        group_service.update_group(
            uow,
            group_id=1,
            name="Updated",
        )

    uow.group_repo.update.assert_not_called()


def test_delete_group(group_service, uow):
    uow.group_repo.get.return_value = SimpleNamespace(id=1)

    group_service.delete_group(
        uow,
        group_id=1,
    )

    uow.group_repo.delete.assert_called_once_with(1)


def test_delete_group_not_found(group_service, uow):
    uow.group_repo.get.return_value = None

    with pytest.raises(
        GroupNotFoundError,
        match="Group 1 not found",
    ):
        group_service.delete_group(
            uow,
            group_id=1,
        )

    uow.group_repo.delete.assert_not_called()


def test_add_contact(group_service, uow):
    uow.group_repo.get.return_value = SimpleNamespace(id=1)
    uow.contact_repo.get.return_value = SimpleNamespace(id=100)

    group_service.add_contact(
        uow,
        group_id=1,
        contact_id=100,
    )

    uow.group_repo.add_contact.assert_called_once_with(
        group_id=1,
        contact_id=100,
    )


def test_add_contact_group_not_found(group_service, uow):
    uow.group_repo.get.return_value = None

    with pytest.raises(
        GroupNotFoundError,
        match="Group 1 not found",
    ):
        group_service.add_contact(
            uow,
            group_id=1,
            contact_id=100,
        )

    uow.group_repo.add_contact.assert_not_called()


def test_add_contact_contact_not_found(group_service, uow):
    uow.group_repo.get.return_value = SimpleNamespace(id=1)
    uow.contact_repo.get.return_value = None

    with pytest.raises(
        ContactNotFoundError,
        match="Contact 100 not found",
    ):
        group_service.add_contact(
            uow,
            group_id=1,
            contact_id=100,
        )

    uow.group_repo.add_contact.assert_not_called()


def test_remove_contact(group_service, uow):
    uow.group_repo.get.return_value = SimpleNamespace(id=1)
    uow.contact_repo.get.return_value = SimpleNamespace(id=100)

    group_service.remove_contact(
        uow,
        group_id=1,
        contact_id=100,
    )

    uow.group_repo.remove_contact_from_group.assert_called_once_with(
        group_id=1,
        contact_id=100,
    )


def test_remove_contact_group_not_found(group_service, uow):
    uow.group_repo.get.return_value = None

    with pytest.raises(
        GroupNotFoundError,
        match="Group 1 not found",
    ):
        group_service.remove_contact(
            uow,
            group_id=1,
            contact_id=100,
        )

    uow.group_repo.remove_contact_from_group.assert_not_called()


def test_remove_contact_contact_not_found(group_service, uow):
    uow.group_repo.get.return_value = SimpleNamespace(id=1)
    uow.contact_repo.get.return_value = None

    with pytest.raises(
        ContactNotFoundError,
        match="Contact 100 not found",
    ):
        group_service.remove_contact(
            uow,
            group_id=1,
            contact_id=100,
        )

    uow.group_repo.remove_contact_from_group.assert_not_called()


def test_get_contacts(group_service, uow):
    group = SimpleNamespace(id=1)
    contacts = [SimpleNamespace(id=100)]

    uow.group_repo.get.return_value = group
    uow.group_repo.get_with_contacts.return_value = contacts

    result = group_service.get_contacts(
        uow,
        group_id=1,
    )

    assert result == contacts

    uow.group_repo.get_with_contacts.assert_called_once_with(
        group_id=1,
    )


def test_get_contacts_group_not_found(group_service, uow):
    uow.group_repo.get.return_value = None

    with pytest.raises(
        GroupNotFoundError,
        match="Group 1 not found",
    ):
        group_service.get_contacts(
            uow,
            group_id=1,
        )

    uow.group_repo.get_with_contacts.assert_not_called()
