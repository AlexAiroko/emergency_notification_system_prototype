from sqlalchemy.exc import IntegrityError

from app.db.uow import UnitOfWork
from app.exceptions.contact import ContactNotFoundError
from app.exceptions.group import GroupAlreadyExistsError, GroupNotFoundError
from app.models.group import Group


class GroupService:
    def create_group(
        self,
        uow: UnitOfWork,
        name: str,
    ) -> Group:
        try:
            return uow.group_repo.create(name=name)
        except IntegrityError:
            raise GroupAlreadyExistsError()
    
    def get_group(
        self,
        uow: UnitOfWork,
        group_id: int,
    ) -> Group:
        group = uow.group_repo.get_with_contacts(group_id)

        if group is None:
            raise GroupNotFoundError(group_id)

        return group
    
    def get_many_groups(
        self,
        uow: UnitOfWork,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Group]:
        return uow.group_repo.get_many(
            limit=limit,
            offset=offset,
        )
    
    def update_group(
        self,
        uow: UnitOfWork,
        group_id: int,
        name: str,
    ) -> None:
        group = uow.group_repo.get(group_id)

        if group is None:
            raise GroupNotFoundError(group_id)

        uow.group_repo.update(
            obj_id=group_id,
            name=name,
        )
    
    def delete_group(
        self,
        uow: UnitOfWork,
        group_id: int,
    ) -> None:
        group = uow.group_repo.get(group_id)

        if group is None:
            raise GroupNotFoundError(group_id)

        uow.group_repo.delete(group_id)
    
    def add_contact(
        self,
        uow: UnitOfWork,
        group_id: int,
        contact_id: int,
    ) -> None:
        group = uow.group_repo.get(group_id)

        if group is None:
            raise GroupNotFoundError(group_id)
        
        contact = uow.contact_repo.get(contact_id)
        
        if contact is None:
            raise ContactNotFoundError(contact_id)
        
        uow.group_repo.add_contact(
            group_id=group_id,
            contact_id=contact_id,
        )
    
    def remove_contact(
        self,
        uow: UnitOfWork,
        group_id: int,
        contact_id: int,
    ) -> None:
        group = uow.group_repo.get(group_id)

        if group is None:
            raise GroupNotFoundError(group_id)
        
        contact = uow.contact_repo.get(contact_id)
        
        if contact is None:
            raise ContactNotFoundError(contact_id)
        
        uow.group_repo.remove_contact_from_group(
            group_id=group_id,
            contact_id=contact_id,
        )
    
    def get_contacts(
        self,
        uow: UnitOfWork,
        group_id: int,
    ):
        group = uow.group_repo.get(group_id)

        if group is None:
            raise GroupNotFoundError(group_id)
        
        return uow.group_repo.get_with_contacts(group_id=group_id)
