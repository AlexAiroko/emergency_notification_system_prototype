from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from app.models.contact import Contact
from app.models.group import Group
from app.models.group_contact import GroupContact
from app.repositories.base import BaseRepository


class GroupRepository(BaseRepository):
    def create(self, name: str) -> Group:
        group = Group(name=name)
        self.session.add(group)
        self.flush()
        return group
    
    def get(self, group_id: int) -> Group | None:
        stmt = (
            select(Group)
            .where(Group.id == group_id)
        )
        res = self.session.execute(stmt)
        group = res.scalar_one_or_none()
        return group
    
    def get_with_contacts(self, group_id: int) -> Group | None:
        stmt = (
            select(Group)
            .options(selectinload(Group.contacts))
            .where(Group.id == group_id)
        )
        res = self.session.execute(stmt)
        group = res.scalar_one_or_none()
        return group
    
    def add_contact(self, group_id: int, contact_id: int) -> None:
        link = GroupContact(
            group_id=group_id,
            contact_id=contact_id,
        )
        self.session.add(link)

    def remove_contact_from_group(self, group_id: int, contact_id: int) -> None:
        stmt = (
            delete(GroupContact)
            .where(
                GroupContact.group_id == group_id,
                GroupContact.contact_id == contact_id,
            )
        )
        
        self.session.execute(stmt)
    
    def get_contacts_for_dispatch(self, group_id: int) -> list[Contact]:
        stmt = (
            select(Contact)
            .join(GroupContact, GroupContact.contact_id == Contact.id)
            .where(GroupContact.group_id == group_id)
            .options(selectinload(Contact.contact_methods))
        )
        res = self.session.execute(stmt)
        contacts = list(res.scalars().all())
        return contacts
