import logging

from sqlalchemy.exc import IntegrityError

from app.db.uow import UnitOfWork
from app.exceptions.contact import (
    ContactAlreadyExistsError,
    ContactNotFoundError,
)
from app.models.contact import Contact

logger = logging.getLogger(__name__)


class ContactService:
    def create_contact(
        self,
        uow: UnitOfWork,
        external_id: str | None,
        name: str,
        is_active: bool = True,
    ) -> Contact:
        """
        Creates a new contact.
        """

        try:
            contact = uow.contact_repo.create(
                name=name,
                external_id=external_id,
                is_active=is_active,
            )
        except IntegrityError as exc:
            logger.warning(
                "Contact with external_id=%s already exists",
                external_id,
            )
            raise ContactAlreadyExistsError() from exc

        logger.info(
            "Created contact %s (name=%s)",
            contact.id,
            contact.name,
        )

        return contact

    def get_contact(
        self,
        uow: UnitOfWork,
        contact_id: int,
    ) -> Contact:
        """
        Returns a contact by ID.
        """

        contact = uow.contact_repo.get(contact_id)

        if contact is None:
            logger.warning(
                "Contact %s not found",
                contact_id,
            )
            raise ContactNotFoundError(contact_id)

        return contact

    def update_contact(
        self,
        uow: UnitOfWork,
        contact_id: int,
        name: str,
    ) -> None:
        contact = uow.contact_repo.get(contact_id)

        if contact is None:
            logger.warning(
                "Contact %s not found",
                contact_id,
            )
            raise ContactNotFoundError(contact_id)

        uow.contact_repo.update(
            contact_id,
            name=name,
        )

        logger.info(
            "Updated contact %s",
            contact_id,
        )
