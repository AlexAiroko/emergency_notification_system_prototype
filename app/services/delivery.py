from sqlalchemy.orm import Session

from app.models.contact_method import ChannelType
from app.models.delivery import DeliveryStatus
from app.providers.base import BaseProvider, ProviderError
from app.providers.email import EmailProvider
from app.providers.provider_registry import ProviderRegistry
from app.providers.telegram import TelegramProvider
from app.repositories.delivery import DeliveryRepository
from app.repositories.notification import NotificationRepository
from app.services.notification_template import NotificationTemplateService


class DeliveryService:
    def __init__(self, session: Session) -> None:
        self.session = session
        
        self.delivery_repo = DeliveryRepository(session)
        self.notification_repo = NotificationRepository(session)
        
        self.template_service = NotificationTemplateService(session)
        
        self.provider_registry = ProviderRegistry()

    def send(self, delivery_id: int) -> None:
        """
        Sends one Delivery.

        Algorithm:
        1. Loads the Delivery.
        2. Selects a provider by channel.
        3. Sends the message.
        4. If successful, marks the Delivery as SENT.
        5. If an error occurs, marks the Delivery as FAILED.
        """
        delivery = self.delivery_repo.get(delivery_id)
        
        if delivery is None:
            raise ValueError(f"Delivery {delivery_id} not found")

        notification = self.notification_repo.get_with_relations(delivery.notification_id)
        
        if notification is None:
            raise ValueError(
                f"Notification {delivery.notification_id} not found"
            )
        
        template = self.template_service.ensure_template_is_active(
            notification.template_id
        )

        provider = self.provider_registry.get(delivery.channel)
        
        try:
            provider_message_id = provider.send(
                to=delivery.address,
                subject=template.subject,
                body=template.body,
            )

            self.delivery_repo.mark_sent(
                delivery.id,
                provider_message_id=provider_message_id,
            )
        except ProviderError as exc:
            self.delivery_repo.mark_failed(
                delivery.id,
                error_message=str(exc),
            )
    
    def send_pending(self, notification_id: int) -> None:
        """
        Sends all Deliveries with a PENDING status for the specified Notification.
        """
        deliveries = self.delivery_repo.get_by_notification(notification_id)
        
        for delivery in deliveries:
            if delivery.status == DeliveryStatus.PENDING:
                self.send(delivery.id)
