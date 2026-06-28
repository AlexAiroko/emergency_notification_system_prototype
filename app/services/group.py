import logging

from sqlalchemy.exc import IntegrityError

from app.db.uow import UnitOfWork
from app.exceptions.contact import ContactNotFoundError
from app.exceptions.group import GroupAlreadyExistsError, GroupNotFoundError
from app.models.group import Group


logger = logging.getLogger(__name__)


class GroupService:
    def create_group(
        self,
        uow: UnitOfWork,
        name: str,
    ) -> Group:
        try:
            group = uow.group_repo.create(name=name)
        except IntegrityError as exc:
            logger.warning(
                "Failed to create group: group with name '%s' already exists",
                name,
            )
            raise GroupAlreadyExistsError() from exc
        
        logger.info(
                "Created group %s (name=%s)",
                group.id,
                group.name,
            )

        return group
    
    def get_group(
        self,
        uow: UnitOfWork,
        group_id: int,
    ) -> Group:
        group = uow.group_repo.get_with_contacts(group_id)

        if group is None:
            logger.warning(
                "Group %s not found",
                group_id,
            )
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
            logger.warning(
                "Group %s not found",
                group_id,
            )
            raise GroupNotFoundError(group_id)

        uow.group_repo.update(
            obj_id=group_id,
            name=name,
        )
        
        logger.info(
            "Updated group %s",
            group_id,
        )
    
    def delete_group(
        self,
        uow: UnitOfWork,
        group_id: int,
    ) -> None:
        group = uow.group_repo.get(group_id)

        if group is None:
            logger.warning(
                "Group %s not found",
                group_id,
            )
            raise GroupNotFoundError(group_id)

        uow.group_repo.delete(group_id)
        
        logger.info(
            "Deleted group %s",
            group_id,
        )
    
    def add_contact(
        self,
        uow: UnitOfWork,
        group_id: int,
        contact_id: int,
    ) -> None:
        group = uow.group_repo.get(group_id)

        if group is None:
            logger.warning(
                "Group %s not found",
                group_id,
            )
            raise GroupNotFoundError(group_id)
        
        contact = uow.contact_repo.get(contact_id)
        
        if contact is None:
            logger.warning(
                "Contact %s not found",
                contact_id,
            )
            raise ContactNotFoundError(contact_id)
        
        uow.group_repo.add_contact(
            group_id=group_id,
            contact_id=contact_id,
        )
        
        logger.info(
            "Added contact %s to group %s",
            contact_id,
            group_id,
        )
    
    def remove_contact(
        self,
        uow: UnitOfWork,
        group_id: int,
        contact_id: int,
    ) -> None:
        group = uow.group_repo.get(group_id)

        if group is None:
            logger.warning(
                "Group %s not found",
                group_id,
            )
            raise GroupNotFoundError(group_id)
        
        contact = uow.contact_repo.get(contact_id)
        
        if contact is None:
            logger.warning(
                "Contact %s not found",
                contact_id,
            )
            raise ContactNotFoundError(contact_id)
        
        uow.group_repo.remove_contact_from_group(
            group_id=group_id,
            contact_id=contact_id,
        )
        
        logger.info(
            "Removed contact %s from group %s",
            contact_id,
            group_id,
        )
    
    def get_contacts(
        self,
        uow: UnitOfWork,
        group_id: int,
    ):
        group = uow.group_repo.get(group_id)

        if group is None:
            logger.warning(
                "Group %s not found",
                group_id,
            )
            raise GroupNotFoundError(group_id)
        
        return uow.group_repo.get_with_contacts(group_id=group_id)
