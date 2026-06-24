from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.exceptions.contact import ContactNotFoundError
from app.models.contact_method import ChannelType


def test_create_method(contact_method_service, uow):
    contact = SimpleNamespace(id=1)
    method = SimpleNamespace(id=10)

    uow.contact_repo.get.return_value = contact
    uow.contact_method_repo.create.return_value = method

    result = contact_method_service.create_method(
        uow,
        contact_id=1,
        channel=ChannelType.EMAIL,
        address="user@mail.com",
    )

    assert result is method

    uow.contact_repo.get.assert_called_once_with(1)

    uow.contact_method_repo.create.assert_called_once_with(
        contact_id=1,
        channel=ChannelType.EMAIL,
        address="user@mail.com",
    )


def test_create_method_contact_not_found(contact_method_service, uow):
    uow.contact_repo.get.return_value = None

    with pytest.raises(
        ContactNotFoundError,
        match="Contact 1 not found",
    ):
        contact_method_service.create_method(
            uow,
            contact_id=1,
            channel=ChannelType.EMAIL,
            address="user@mail.com",
        )

    uow.contact_method_repo.create.assert_not_called()


def test_get_method(contact_method_service, uow):
    contact = SimpleNamespace(id=1)
    method = SimpleNamespace(id=10)

    uow.contact_repo.get.return_value = contact
    uow.contact_method_repo.get.return_value = method

    result = contact_method_service.get_method(
        uow,
        contact_id=1,
        method_id=10,
    )

    assert result is method

    uow.contact_method_repo.get.assert_called_once_with(10)


def test_get_method_contact_not_found(contact_method_service, uow):
    uow.contact_repo.get.return_value = None

    with pytest.raises(
        ContactNotFoundError,
        match="Contact 1 not found",
    ):
        contact_method_service.get_method(
            uow,
            contact_id=1,
            method_id=10,
        )

    uow.contact_method_repo.get.assert_not_called()


def test_get_methods(contact_method_service, uow):
    contact = SimpleNamespace(id=1)
    methods = [Mock(), Mock()]

    uow.contact_repo.get.return_value = contact
    uow.contact_method_repo.get_by_contact.return_value = methods

    result = contact_method_service.get_methods(
        uow,
        contact_id=1,
    )

    assert result == methods

    uow.contact_method_repo.get_by_contact.assert_called_once_with(1)


def test_get_methods_contact_not_found(contact_method_service, uow):
    uow.contact_repo.get.return_value = None

    with pytest.raises(
        ContactNotFoundError,
        match="Contact 1 not found",
    ):
        contact_method_service.get_methods(
            uow,
            contact_id=1,
        )

    uow.contact_method_repo.get_by_contact.assert_not_called()


def test_update_method(contact_method_service, uow):
    method = SimpleNamespace(
        id=10,
        contact_id=1,
    )

    uow.contact_method_repo.get.return_value = method

    contact_method_service.update_method(
        uow,
        contact_id=1,
        method_id=10,
        channel=ChannelType.EMAIL,
        address="new@mail.com",
        is_active=False,
    )

    uow.contact_method_repo.update.assert_called_once_with(
        10,
        channel=ChannelType.EMAIL,
        address="new@mail.com",
        is_active=False,
    )


def test_update_method_not_found(contact_method_service, uow):
    uow.contact_method_repo.get.return_value = None

    with pytest.raises(
        ContactNotFoundError,
        match="Contact 1 not found",
    ):
        contact_method_service.update_method(
            uow,
            contact_id=1,
            method_id=10,
            channel=ChannelType.EMAIL,
            address="new@mail.com",
            is_active=True,
        )

    uow.contact_method_repo.update.assert_not_called()


def test_update_method_belongs_to_other_contact(
    contact_method_service,
    uow,
):
    method = SimpleNamespace(
        id=10,
        contact_id=999,
    )

    uow.contact_method_repo.get.return_value = method

    with pytest.raises(
        ContactNotFoundError,
        match="Contact 1 not found",
    ):
        contact_method_service.update_method(
            uow,
            contact_id=1,
            method_id=10,
            channel=ChannelType.EMAIL,
            address="new@mail.com",
            is_active=True,
        )

    uow.contact_method_repo.update.assert_not_called()


def test_delete_method(contact_method_service, uow):
    method = SimpleNamespace(
        id=10,
        contact_id=1,
    )

    uow.contact_method_repo.get.return_value = method

    contact_method_service.delete_method(
        uow,
        contact_id=1,
        method_id=10,
    )

    uow.contact_method_repo.delete.assert_called_once_with(10)


def test_delete_method_not_found(contact_method_service, uow):
    uow.contact_method_repo.get.return_value = None

    with pytest.raises(
        ContactNotFoundError,
        match="Contact 1 not found",
    ):
        contact_method_service.delete_method(
            uow,
            contact_id=1,
            method_id=10,
        )

    uow.contact_method_repo.delete.assert_not_called()


def test_delete_method_belongs_to_other_contact(
    contact_method_service,
    uow,
):
    method = SimpleNamespace(
        id=10,
        contact_id=999,
    )

    uow.contact_method_repo.get.return_value = method

    with pytest.raises(
        ContactNotFoundError,
        match="Contact 1 not found",
    ):
        contact_method_service.delete_method(
            uow,
            contact_id=1,
            method_id=10,
        )

    uow.contact_method_repo.delete.assert_not_called()
