from fastapi import APIRouter, Depends, status

from app.db.deps import get_uow
from app.db.uow import UnitOfWork
from app.schemas.contact import ContactResponse
from app.schemas.group import GroupCreate, GroupResponse, GroupUpdate, GroupWithContactsResponse
from app.services.group import GroupService


router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
)


@router.post(
    "",
    response_model=GroupResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_group(
    data: GroupCreate,
    uow: UnitOfWork = Depends(get_uow),
):
    service = GroupService()
    
    group = service.create_group(
        uow=uow,
        name=data.name,
    )
    
    return group


@router.get(
    "/{group_id}",
    response_model=GroupWithContactsResponse,
)
def get_group(
    group_id: int,
    uow: UnitOfWork = Depends(get_uow),
):
    service = GroupService()
    
    group = service.get_group(
        uow=uow,
        group_id=group_id,
    )
    
    return group


@router.get(
    "",
    response_model=list[GroupResponse],
)
def get_groups(
    limit: int = 20,
    offset: int = 0,
    uow: UnitOfWork = Depends(get_uow),
):
    service = GroupService()
    return service.get_many_groups(
        uow,
        limit=limit,
        offset=offset,
    )


@router.patch(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_group(
    group_id: int,
    data: GroupUpdate,
    uow: UnitOfWork = Depends(get_uow),
):
    service = GroupService()

    service.update_group(
        uow=uow,
        group_id=group_id,
        name=data.name,
    )


@router.delete(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_group(
    group_id: int,
    uow: UnitOfWork = Depends(get_uow),
):
    service = GroupService()

    service.delete_group(
        uow=uow,
        group_id=group_id,
    )


@router.post(
    "/{group_id}/contacts/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def add_contact_to_group(
    group_id: int,
    contact_id: int,
    uow: UnitOfWork = Depends(get_uow),
):
    service = GroupService()

    service.add_contact(
        uow=uow,
        group_id=group_id,
        contact_id=contact_id,
    )


@router.delete(
    "/{group_id}/contacts/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_contact_from_group(
    group_id: int,
    contact_id: int,
    uow: UnitOfWork = Depends(get_uow),
):
    service = GroupService()

    service.remove_contact(
        uow=uow,
        group_id=group_id,
        contact_id=contact_id,
    )


@router.get(
    "/{group_id}/contacts",
    response_model=list[ContactResponse],
)
def get_group_contacts(
    group_id: int,
    uow: UnitOfWork = Depends(get_uow),
):
    service = GroupService()

    group = service.get_contacts(
        uow=uow,
        group_id=group_id,
    )

    return group.contacts
