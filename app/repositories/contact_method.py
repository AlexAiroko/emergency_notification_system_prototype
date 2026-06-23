from sqlalchemy import select

from app.models.contact_method import ChannelType, ContactMethod
from app.repositories.active import ActiveRepository


class ContactMethodRepository(ActiveRepository):
    model = ContactMethod
    
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
