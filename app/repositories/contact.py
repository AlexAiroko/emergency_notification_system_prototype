from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.contact import Contact
from app.repositories.active import ActiveRepository


class ContactRepository(ActiveRepository):
    model = Contact
    
    def get_with_methods(self, contact_id: int) -> Contact | None:
        stmt = (
            select(Contact)
            .options(selectinload(Contact.contact_methods))
            .where(Contact.id == contact_id)
        )
        res = self.session.execute(stmt)
        contact = res.scalar_one_or_none()
        return contact
