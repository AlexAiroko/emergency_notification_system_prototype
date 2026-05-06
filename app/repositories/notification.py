from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.models.notification import Notification, NotificationStatus
from app.repositories.base import BaseRepository


class NotificationRepository(BaseRepository):
    def create(self, template_id: int, group_id: int) -> Notification:
        notification = Notification(
            template_id=template_id,
            group_id=group_id,
        )
        
        self.session.add(notification)
        self.flush()
        return notification
    
    def get(self, notification_id: int) -> Notification | None:
        stmt = (
            select(Notification)
            .where(Notification.id == notification_id)
        )
        res = self.session.execute(stmt)
        notification = res.scalar_one_or_none()
        return notification
    
    def get_with_relations(self, notification_id: int) -> Notification | None:
        stmt = (
            select(Notification)
            .options(
                selectinload(Notification.template),
                selectinload(Notification.group),
            )
            .where(Notification.id == notification_id)
        )
        res = self.session.execute(stmt)
        notification = res.scalar_one_or_none()
        return notification
    
    def update_status(self, notification_id: int, status: NotificationStatus) -> None:
        stmt = (
            update(Notification)
            .where(Notification.id == notification_id)
            .values(status=status)
        )
        self.session.execute(stmt)
    
    def mark_started(self, notification_id: int) -> None:
        self.update_status(notification_id, NotificationStatus.IN_PROGRESS)
    
    def mark_finished(self, notification_id: int) -> None:
        self.update_status(notification_id, NotificationStatus.SUCCESS)
        
