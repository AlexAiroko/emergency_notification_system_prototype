from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.models.contact import Contact
from app.repositories.base import BaseRepository


class ContactRepository(BaseRepository):
    def create(
            self,
            name: str, 
            external_id: str | None = None, 
            is_active: bool = True,
        ) -> Contact:
        contact = Contact(
            name=name,
            external_id=external_id,
            is_active=is_active,
        )
        self.session.add(contact)
        self.flush()
        return contact
    
    def get(self, contact_id: int) -> Contact | None:
        stmt = (
            select(Contact)
            .where(Contact.id == contact_id)
        )
        res = self.session.execute(stmt)
        contact = res.scalar_one_or_none()
        return contact
    
    def get_many(self, limit: int = 20, offset: int = 0) -> list[Contact]:
        stmt = (
            select(Contact)
            .order_by(Contact.id)
            .limit(limit)
            .offset(offset)
        )
        res = self.session.execute(stmt)
        contacts = list(res.scalars().all())
        return contacts
    
    def get_active(self, limit: int = 20, offset: int = 0) -> list[Contact]:
        stmt = (
            select(Contact)
            .where(Contact.is_active)
            .order_by(Contact.id)
            .limit(limit)
            .offset(offset)
        )
        res = self.session.execute(stmt)
        contacts = list(res.scalars().all())
        return contacts
    
    def get_with_methods(self, contact_id: int) -> Contact | None:
        stmt = (
            select(Contact)
            .options(selectinload(Contact.contact_methods))
            .where(Contact.id == contact_id)
        )
        res = self.session.execute(stmt)
        contact = res.scalar_one_or_none()
        return contact
    
    def update(self, contact_id: int, name: str) -> None:
        stmt = (
            update(Contact)
            .where(Contact.id == contact_id)
            .values(name=name)
        )
        self.session.execute(stmt)

    def activate(self, contact_id: int) -> None:
        self._set_active(contact_id, True)
    
    def deactivate(self, contact_id: int) -> None:
        self._set_active(contact_id, False)
    
    def _set_active(
        self,
        contact_id: int,
        is_active: bool,
    ) -> None:
        stmt = (
            update(Contact)
            .where(Contact.id == contact_id)
            .values(is_active=is_active)
        )
        self.session.execute(stmt)
