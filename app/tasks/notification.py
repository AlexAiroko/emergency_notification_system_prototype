from app.db.uow import UnitOfWork
from app.services.notification import NotificationService


def send_notification_task(notification_id: int):
    with UnitOfWork() as uow:
        NotificationService().send_notification(
            uow=uow,
            notification_id=notification_id,
        )
