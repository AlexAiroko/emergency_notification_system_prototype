from sqlalchemy import delete, select

from app.models.contact_method import ChannelType, ContactMethod
from app.repositories.base import BaseRepository


class ContactMethodRepository(BaseRepository):
    def create(self, contact_id: int, channel: ChannelType, address: str) -> ContactMethod:
        method = ContactMethod(
            contact_id=contact_id,
            channel=channel,
            address=address,
        )
        self.session.add(method)
        self.flush()
        return method

    def get(self, method_id: int) -> ContactMethod | None:
        stmt = (
            select(ContactMethod)
            .where(ContactMethod.id == method_id)
        )
        res = self.session.execute(stmt)
        method = res.scalar_one_or_none()
        return method

    def get_by_contact(self, contact_id: int) -> list[ContactMethod]:
        stmt = (
            select(ContactMethod)
            .where(ContactMethod.contact_id == contact_id)
            .order_by(ContactMethod.id)
        )
        res = self.session.execute(stmt)
        methods = list(res.scalars().all())
        return methods

    def get_by_contact_and_channel(self, contact_id: int, channel: ChannelType) -> list[ContactMethod]:
        stmt = (
            select(ContactMethod)
            .where(
                ContactMethod.contact_id == contact_id,
                ContactMethod.channel == channel,
            )
            .order_by(ContactMethod.id)
        )
        res = self.session.execute(stmt)
        methods = list(res.scalars().all())
        return methods
    
    def delete(self, method_id: int) -> None:
        stmt = (
            delete(ContactMethod)
            .where(ContactMethod.id == method_id)
        )
        self.session.execute(stmt)
