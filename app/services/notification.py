from sqlalchemy.orm import Session

from app.models.delivery import Delivery, DeliveryStatus
from app.models.notification import Notification, NotificationStatus
from app.repositories.delivery import DeliveryRepository
from app.repositories.group import GroupRepository
from app.repositories.notification import NotificationRepository
from app.services.delivery import DeliveryService
from app.services.notification_template import NotificationTemplateService


class NotificationService:
    def __init__(self, session: Session) -> None:
        self.session = session
        
        self.notification_repo = NotificationRepository(session)
        self.group_repo = GroupRepository(session)
        self.delivery_repo = DeliveryRepository(session)
        
        self.delivery_service = DeliveryService(session)
        self.template_service = NotificationTemplateService(session)

    def create_notification(
        self,
        template_id: int,
        group_id: int,
    ) -> Notification:
        """
        Creates a Notification with the PENDING status and generates a Delivery 
        for each ContactMethod of each contact in the group.
        """
        
        self.template_service.ensure_template_is_active(template_id)
        
        notification = self.notification_repo.create(
            template_id=template_id,
            group_id=group_id,
        )
        
        contacts = self.group_repo.get_contacts_for_dispatch(group_id)
        
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
        
        if deliveries:
            self.delivery_repo.create_bulk(deliveries)
        
        return notification

    def start_notification(self, notification_id: int) -> None:
        """
        Sets the notification to IN_PROGRESS.
        """
        self.notification_repo.mark_started(notification_id)

    def send_notification(self, notification_id: int) -> None:
        """
        The full notification sending cycle:
        1. Sets the notification to IN_PROGRESS
        2. Sends all pending deliveries
        3. Finalizes the notification status
        """
        self.start_notification(notification_id)

        self.delivery_service.send_pending(notification_id)

        self.finalize_notification(notification_id)

    def finalize_notification(self, notification_id: int) -> None:
        """
        Calculates the final Notification status based on Delivery statistics.

        Rules:
        - all SENT -> SUCCESS
        - all FAILED -> FAILED
        - part SENT and part FAILED -> PARTIAL_SUCCESS
        """
        stats = self.delivery_repo.get_stats(notification_id)
        
        sent = stats.get("sent", 0)
        failed = stats.get("failed", 0)
        
        total = sent + failed
        
        if total == 0:
            return
        
        if sent == total:
            status = NotificationStatus.SUCCESS
        elif failed == total:
            status = NotificationStatus.FAILED
        else:
            status = NotificationStatus.PARTIAL_SUCCESS
        
        self.notification_repo.update_status(
            notification_id,
            status,
        )
