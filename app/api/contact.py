from fastapi import APIRouter, Depends, status

from app.db.deps import get_uow
from app.db.uow import UnitOfWork
from app.schemas.contact import ContactCreate, ContactResponse, ContactUpdate
from app.services.contact import ContactService


router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"],
)


@router.post(
    "",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_contact(
    data: ContactCreate,
    uow: UnitOfWork = Depends(get_uow),
):
    service = ContactService()
    
    contact = service.create_contact(
        uow=uow,
        external_id=data.external_id,
        name=data.name,
    )
    
    return contact


@router.get(
    "",
    response_model=list[ContactResponse],
)
def get_many_contacts(
    limit: int = 20,
    offset: int = 0,
    uow: UnitOfWork = Depends(get_uow),
):
    return uow.contact_repo.get_many(
        limit=limit,
        offset=offset,
    )


@router.get(
    "/active",
    response_model=list[ContactResponse],
)
def get_active_contacts(
    limit: int = 20,
    offset: int = 0,
    uow: UnitOfWork = Depends(get_uow),
):
    return uow.contact_repo.get_active(
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
)
def get_contact_by_id(
    contact_id: int,
    uow: UnitOfWork = Depends(get_uow),
):
    service = ContactService()

    contact = service.get_contact(uow, contact_id)

    return contact


@router.patch(
    "/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_contact(
    contact_id: int,
    data: ContactUpdate,
    uow: UnitOfWork = Depends(get_uow),
):
    service = ContactService()
    service.update_contact(
        uow=uow,
        contact_id=contact_id,
        name=data.name,
    )


@router.patch(
    "/{contact_id}/activate",
    status_code=status.HTTP_204_NO_CONTENT,
)
def activate_contact(
    contact_id: int,
    uow: UnitOfWork = Depends(get_uow),
):
    uow.contact_repo.activate(contact_id)


@router.patch(
    "/{contact_id}/deactivate",
    status_code=status.HTTP_204_NO_CONTENT,
)
def deactivate_contact(
    contact_id: int,
    uow: UnitOfWork = Depends(get_uow),
):
    uow.contact_repo.deactivate(contact_id)
