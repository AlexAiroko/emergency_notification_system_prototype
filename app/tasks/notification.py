import logging

from app.db.uow import UnitOfWork
from app.services.notification import NotificationService


logger = logging.getLogger(__name__)


def send_notification_task(notification_id: int):
    logger.info(
        "Background task started (notification_id=%s)",
        notification_id,
    )

    try:
        with UnitOfWork() as uow:
            NotificationService().send_notification(
                uow=uow,
                notification_id=notification_id,
            )

        logger.info(
            "Background task finished successfully (notification_id=%s)",
            notification_id,
        )

    except Exception as exc:
        logger.exception(
            "Background task failed (notification_id=%s)",
            notification_id,
        )
        raise
