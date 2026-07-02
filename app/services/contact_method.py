import logging

from app.db.uow import UnitOfWork
from app.exceptions.contact import ContactNotFoundError
from app.exceptions.contact_method import ContactMethodNotFoundError
from app.models.contact_method import ChannelType, ContactMethod
from app.validators.contact_methods.registry import ContactMethodValidatorRegistry

logger = logging.getLogger(__name__)


class ContactMethodService:
    def create_method(
        self,
        uow: UnitOfWork,
        contact_id: int,
        channel: ChannelType,
        address: str,
    ) -> ContactMethod:
        contact = uow.contact_repo.get(contact_id)

        if contact is None:
            logger.warning(
                "Contact %s not found",
                contact_id,
            )
            raise ContactNotFoundError(contact_id)

        address = ContactMethodValidatorRegistry.validate(
            channel=channel,
            value=address,
        )

        method = uow.contact_method_repo.create(
            contact_id=contact_id,
            channel=channel,
            address=address,
        )

        logger.info(
            "Created contact method %s for contact %s",
            method.id,
            contact_id,
        )

        return method

    def get_method(
        self,
        uow: UnitOfWork,
        contact_id: int,
        method_id: int,
    ) -> ContactMethod | None:
        contact = uow.contact_repo.get(contact_id)

        if contact is None:
            logger.warning(
                "Contact %s not found",
                contact_id,
            )
            raise ContactNotFoundError(contact_id)

        return uow.contact_method_repo.get(method_id)

    def get_methods(
        self,
        uow: UnitOfWork,
        contact_id: int,
    ) -> list[ContactMethod]:
        contact = uow.contact_repo.get(contact_id)

        if contact is None:
            logger.warning(
                "Contact %s not found",
                contact_id,
            )
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

        if method is None or method.contact_id != contact_id:
            logger.warning(
                "Contact method %s not found for contact %s",
                method_id,
                contact_id,
            )
            raise ContactMethodNotFoundError(method_id)

        address = ContactMethodValidatorRegistry.validate(
            channel=channel,
            value=address,
        )

        uow.contact_method_repo.update(
            method_id,
            channel=channel,
            address=address,
            is_active=is_active,
        )

        logger.info(
            "Updated contact method %s",
            method_id,
        )

    def delete_method(
        self,
        uow: UnitOfWork,
        contact_id: int,
        method_id: int,
    ) -> None:
        method = uow.contact_method_repo.get(method_id)

        if method is None or method.contact_id != contact_id:
            logger.warning(
                "Contact method %s not found for contact %s",
                method_id,
                contact_id,
            )
            raise ContactMethodNotFoundError(method_id)

        uow.contact_method_repo.delete(method_id)

        logger.info(
            "Deleted contact method %s",
            method_id,
        )
