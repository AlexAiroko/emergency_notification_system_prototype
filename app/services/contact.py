from sqlalchemy.exc import IntegrityError

from app.db.uow import UnitOfWork
from app.exceptions.contact import ContactAlreadyExistsError, ContactNotFoundError
from app.models.contact import Contact


class ContactService:
    def create_contact(
        self,
        uow: UnitOfWork,
        external_id: str | None,
        name: str,
        is_active: bool = True,
    ) -> Contact:
        """
        Creates a new contact
        """
        
        try:
            contact = uow.contact_repo.create(
                name=name,
                external_id=external_id,
                is_active=is_active,
            )
        except IntegrityError:
            raise ContactAlreadyExistsError()

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
            raise ContactNotFoundError(contact_id)
        
        return contact
