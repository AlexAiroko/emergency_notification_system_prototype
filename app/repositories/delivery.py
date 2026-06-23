from sqlalchemy import func, select, update

from app.models.delivery import Delivery, DeliveryStatus
from app.repositories.base import BaseRepository


class DeliveryRepository(BaseRepository):
    model = Delivery
    
    def create_bulk(self, deliveries: list[Delivery]) -> None:
        self.session.add_all(deliveries)
    
    def get_by_notification(self, notification_id: int) -> list[Delivery]:
        stmt = (
            select(Delivery)
            .where(Delivery.notification_id == notification_id)
        )
        res = self.session.execute(stmt)
        deliveries = list(res.scalars().all())
        return deliveries
    
    def update_status(
        self,
        delivery_id: int,
        status: DeliveryStatus,
    ) -> None:
        stmt = (
            update(Delivery)
            .where(Delivery.id == delivery_id)
            .values(status=status)
        )
        self.session.execute(stmt)
    
    def mark_sent(
        self,
        delivery_id: int,
        provider_message_id: str | None = None,
    ) -> None:
        stmt = (
            update(Delivery)
            .where(Delivery.id == delivery_id)
            .values(
                status=DeliveryStatus.SENT,
                provider_message_id=provider_message_id,
            )
        )
        self.session.execute(stmt)
    
    def mark_failed(
        self,
        delivery_id: int,
        error_message: str,
    ) -> None:
        stmt = (
            update(Delivery)
            .where(Delivery.id == delivery_id)
            .values(
                status=DeliveryStatus.FAILED,
                error_message=error_message,
            )
        )
        self.session.execute(stmt)

    def get_stats(self, notification_id: int) -> dict:
        stmt = (
            select(
                Delivery.status,
                func.count(Delivery.id)
            )
            .where(Delivery.notification_id == notification_id)
            .group_by(Delivery.status)
        )
        rows = self.session.execute(stmt)
        stats = {status.value: count for status, count in rows.all()}
        return stats
