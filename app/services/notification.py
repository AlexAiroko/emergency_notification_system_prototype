import logging

from app.db.uow import UnitOfWork
from app.models.delivery import Delivery, DeliveryStatus
from app.models.notification import Notification, NotificationStatus
from app.services.delivery import DeliveryService
from app.services.notification_template import NotificationTemplateService

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self) -> None:
        self.delivery_service = DeliveryService()
        self.template_service = NotificationTemplateService()

    def create_notification(
        self,
        uow: UnitOfWork,
        template_id: int,
        group_id: int,
    ) -> Notification:
        """
        Creates a Notification with the PENDING status and generates a Delivery
        for each ContactMethod of each contact in the group.
        """

        self.template_service.ensure_template_is_active(
            uow,
            template_id,
        )

        notification = uow.notification_repo.create(
            template_id=template_id,
            group_id=group_id,
        )

        logger.info(
            "Created notification %s (template=%s, group=%s)",
            notification.id,
            template_id,
            group_id,
        )

        contacts = uow.group_repo.get_contacts_for_dispatch(group_id)

        logger.info(
            "Found %s contacts for notification %s",
            len(contacts),
            notification.id,
        )

        deliveries = []

        for contact in contacts:
            for method in contact.contact_methods:
                deliveries.append(
                    Delivery(
                        notification_id=notification.id,
                        contact_id=contact.id,
                        contact_method_id=method.id,
                        channel=method.channel,
                        address=method.address,
                        status=DeliveryStatus.PENDING,
                    )
                )

        if not deliveries:
            logger.warning(
                "No deliveries were created for notification %s",
                notification.id,
            )
            return notification

        uow.delivery_repo.create_bulk(deliveries)

        logger.info(
            "Prepared %s deliveries for notification %s",
            len(deliveries),
            notification.id,
        )

        return notification

    def start_notification(
        self,
        uow: UnitOfWork,
        notification_id: int,
    ) -> None:
        """
        Sets the notification to IN_PROGRESS.
        """
        
        uow.notification_repo.mark_started(notification_id)

    def send_notification(
        self,
        uow: UnitOfWork,
        notification_id: int,
    ) -> None:
        """
        The full notification sending cycle:
        1. Sets the notification to IN_PROGRESS
        2. Sends all pending deliveries
        3. Finalizes the notification status
        """

        logger.info(
            "Started sending notification %s",
            notification_id,
        )

        self.start_notification(
            uow,
            notification_id,
        )

        self.delivery_service.send_pending(
            uow,
            notification_id,
        )

        self.finalize_notification(
            uow,
            notification_id,
        )

        logger.info(
            "Finished sending notification %s",
            notification_id,
        )

    def finalize_notification(
        self,
        uow: UnitOfWork,
        notification_id: int,
    ) -> None:
        """
        Calculates the final Notification status based on Delivery statistics.

        Rules:
        - all SENT -> SUCCESS
        - all FAILED -> FAILED
        - part SENT and part FAILED -> PARTIAL_SUCCESS
        """

        stats = uow.delivery_repo.get_stats(notification_id)

        sent = stats.get("sent", 0)
        failed = stats.get("failed", 0)

        total = sent + failed

        if total == 0:
            logger.warning(
                "Finished notification %s without deliveries",
                notification_id,
            )
            return

        if sent == total:
            status = NotificationStatus.SUCCESS
        elif failed == total:
            status = NotificationStatus.FAILED
        else:
            status = NotificationStatus.PARTIAL_SUCCESS

        uow.notification_repo.update_status(
            notification_id,
            status,
        )

        logger.info(
            "Finalized notification %s (status=%s, sent=%s, failed=%s)",
            notification_id,
            status.value,
            sent,
            failed,
        )
