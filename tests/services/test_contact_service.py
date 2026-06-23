from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from sqlalchemy.exc import IntegrityError

from app.exceptions.contact import ContactAlreadyExistsError, ContactNotFoundError
from app.services.contact import ContactService


def test_create_contact_success(contact_service, uow):
    contact = SimpleNamespace(id=1, name="John")

    uow.contact_repo.create.return_value = contact

    result = contact_service.create_contact(
        uow=uow,
        name="John",
        external_id="ext-1",
    )

    assert result is contact

    uow.contact_repo.create.assert_called_once_with(
        name="John",
        external_id="ext-1",
        is_active=True,
    )


def test_create_contact_already_exists(contact_service, uow):
    uow.contact_repo.create.side_effect = IntegrityError(
        statement="",
        params={},
        orig=Exception(),
    )

    with pytest.raises(ContactAlreadyExistsError):
        contact_service.create_contact(
            uow=uow,
            name="John",
            external_id="ext-1",
        )


def test_get_contact_success(contact_service, uow):
    contact = SimpleNamespace(id=1, name="John")

    uow.contact_repo.get.return_value = contact

    result = contact_service.get_contact(
        uow=uow,
        contact_id=1,
    )

    assert result is contact

    uow.contact_repo.get.assert_called_once_with(1)


def test_get_contact_not_found(contact_service, uow):
    uow.contact_repo.get.return_value = None

    with pytest.raises(ContactNotFoundError):
        contact_service.get_contact(
            uow=uow,
            contact_id=999,
        )

    uow.contact_repo.get.assert_called_once_with(999)


def test_update_contact_success(contact_service, uow):
    contact = SimpleNamespace(id=1, name="Old")

    uow.contact_repo.get.return_value = contact

    contact_service.update_contact(
        uow=uow,
        contact_id=1,
        name="New Name",
    )

    uow.contact_repo.get.assert_called_once_with(1)

    uow.contact_repo.update.assert_called_once_with(
        1,
        name="New Name",
    )


def test_update_contact_not_found(contact_service, uow):
    uow.contact_repo.get.return_value = None

    with pytest.raises(ContactNotFoundError) as exc:
        contact_service.update_contact(
            uow=uow,
            contact_id=999,
            name="New Name",
        )

    assert "999" in str(exc.value)

    uow.contact_repo.get.assert_called_once_with(999)
    uow.contact_repo.update.assert_not_called()
