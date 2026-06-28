from fastapi import APIRouter, BackgroundTasks, Depends, status

from app.db.deps import get_uow
from app.db.uow import UnitOfWork
from app.schemas.delivery import DeliveryResponse
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.services.notification import NotificationService
from app.tasks.notification import send_notification_task


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)

@router.post(
    "",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_notification(
    data: NotificationCreate,
    uow: UnitOfWork = Depends(get_uow),
):
    service = NotificationService()
    
    notification = service.create_notification(
        uow=uow,
        template_id=data.template_id,
        group_id=data.group_id,
    )
    
    return notification


@router.get(
    "",
    response_model=list[NotificationResponse],
)
def get_notifications(
    limit: int = 20,
    offset: int = 0,
    uow: UnitOfWork = Depends(get_uow),
):
    return uow.notification_repo.get_many(
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
)
def get_notification(
    notification_id: int,
    uow: UnitOfWork = Depends(get_uow),
):
    return uow.notification_repo.get(notification_id)

@router.post(
    "/{notification_id}",
)
def send_notification(
    notification_id: int,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(
        send_notification_task,
        notification_id,
    )
    
    return {"message": "Notification started"}


@router.get(
    "/{notification_id}/deliveries",
    response_model=list[DeliveryResponse],
)
def get_deliveries(
    notification_id: int,
    uow: UnitOfWork = Depends(get_uow),
):
    return uow.delivery_repo.get_by_notification(notification_id)


@router.get("/{notification_id}/stats")
def get_notification_stats(
    notification_id: int,
    uow: UnitOfWork = Depends(get_uow),
):
    return uow.delivery_repo.get_stats(notification_id)
