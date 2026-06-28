from app.db.uow import UnitOfWork
from app.exceptions.delivery import DeliveryNotFoundError
from app.exceptions.notification import NotificationNotFoundError
from app.models.delivery import Delivery, DeliveryStatus
from app.providers.base import ProviderError
from app.providers.provider_registry import ProviderRegistry
from app.services.notification_template import NotificationTemplateService


class DeliveryService:
    def __init__(self) -> None:
        self.template_service = NotificationTemplateService()
        
        self.provider_registry = ProviderRegistry()

    def get_delivery(self, uow: UnitOfWork, delivery_id: int) -> Delivery:
        delivery = uow.delivery_repo.get(delivery_id)
        
        if delivery is None:
            raise DeliveryNotFoundError(delivery_id)
        
        return delivery

    def send(self, uow: UnitOfWork, delivery_id: int) -> None:
        """
        Sends one Delivery.

        Algorithm:
        1. Loads the Delivery.
        2. Selects a provider by channel.
        3. Sends the message.
        4. If successful, marks the Delivery as SENT.
        5. If an error occurs, marks the Delivery as FAILED.
        """
        
        delivery = uow.delivery_repo.get(delivery_id)
        
        if delivery is None:
            raise DeliveryNotFoundError(delivery_id)

        notification = uow.notification_repo.get_with_relations(delivery.notification_id)
        
        if notification is None:
            raise NotificationNotFoundError(delivery.notification_id)
        
        template = self.template_service.ensure_template_is_active(
            uow,
            notification.template_id,
        )

        provider = self.provider_registry.get(delivery.channel)
        
        try:
            provider_message_id = provider.send(
                to=delivery.address,
                subject=template.subject,
                body=template.body,
            )

            uow.delivery_repo.mark_sent(
                delivery.id,
                provider_message_id=provider_message_id,
            )
        except ProviderError as exc:
            uow.delivery_repo.mark_failed(
                delivery.id,
                error_message=str(exc),
            )
    
    def send_pending(self, uow: UnitOfWork, notification_id: int) -> None:
        """
        Sends all Deliveries with a PENDING status for the specified Notification.
        """
        deliveries = uow.delivery_repo.get_by_notification(notification_id)
        
        for delivery in deliveries:
            if delivery.status == DeliveryStatus.PENDING:
                self.send(uow, delivery.id)
