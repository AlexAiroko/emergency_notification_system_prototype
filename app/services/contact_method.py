from app.db.uow import UnitOfWork
from app.exceptions.contact import ContactNotFoundError
from app.models.contact_method import ChannelType, ContactMethod


class ContactMethodService:
    def create_method(
        self,
        uow: UnitOfWork,
        contact_id: int,
        channel,
        address: str,
    ) -> ContactMethod:
        contact = uow.contact_repo.get(contact_id)
        if not contact:
            raise ContactNotFoundError(contact_id)

        return uow.contact_method_repo.create(
            contact_id=contact_id,
            channel=channel,
            address=address,
        )

    def get_methods(self, uow: UnitOfWork, contact_id: int):
        contact = uow.contact_repo.get(contact_id)
        if not contact:
            raise ContactNotFoundError(contact_id)

        return uow.contact_method_repo.get_by_contact(contact_id)

    def update_method(
        self,
        uow: UnitOfWork,
        contact_id: int,
        method_id: int,
        channel: ChannelType,
        address: str,
        is_active: bool,
    ) -> None:
        method = uow.contact_method_repo.get(method_id)

        if not method or method.contact_id != contact_id:
            raise ContactNotFoundError(contact_id)

        uow.contact_method_repo.update(
            method_id,
            channel=channel,
            address=address,
            is_active=is_active,
        )

    def delete_method(
        self,
        uow: UnitOfWork,
        contact_id: int,
        method_id: int,
    ) -> None:
        method = uow.contact_method_repo.get(method_id)

        if not method or method.contact_id != contact_id:
            raise ContactNotFoundError(contact_id)

        uow.contact_method_repo.delete(method_id)
