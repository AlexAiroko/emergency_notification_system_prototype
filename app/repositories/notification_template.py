from sqlalchemy import select, update

from app.models.notification_template import NotificationTemplate
from app.repositories.base import BaseRepository


class NotificationTemplateRepository(BaseRepository):
    def create(
        self,
        name: str,
        body: str,
        subject: str | None = None,
        is_active: bool = True,
    ) -> NotificationTemplate:
        template = NotificationTemplate(
            name=name,
            subject=subject,
            body=body,
            is_active=is_active,
        )
        self.session.add(template)
        self.flush()
        return template
    
    def get(self, template_id: int) -> NotificationTemplate | None:
        stmt = (
            select(NotificationTemplate)
            .where(NotificationTemplate.id == template_id)
        )
        res = self.session.execute(stmt)
        template = res.scalar_one_or_none()
        return template
    
    def get_active(self, limit: int = 100, offset: int = 0) -> list[NotificationTemplate]:
        stmt = (
            select(NotificationTemplate)
            .where(NotificationTemplate.is_active)
            .order_by(NotificationTemplate.id)
            .limit(limit)
            .offset(offset)
        )
        res = self.session.execute(stmt)
        templates = list(res.scalars().all())
        return templates
    
    def get_many(self, limit: int = 100, offset: int = 0) -> list[NotificationTemplate]:
        stmt = (
            select(NotificationTemplate)
            .order_by(NotificationTemplate.id)
            .limit(limit)
            .offset(offset)
        )
        res = self.session.execute(stmt)
        templates = list(res.scalars().all())
        return templates
    
    def update_content(self, template_id: int, subject: str, body: str) -> None:
        stmt = (
            update(NotificationTemplate)
            .where(NotificationTemplate.id == template_id)
            .values(
                subject=subject,
                body=body,
            )
        )
        self.session.execute(stmt)

    def activate(self, template_id: int) -> None:
        self._set_active(template_id, True)
    
    def deactivate(self, template_id: int) -> None:
        self._set_active(template_id, False)
    
    def _set_active(
        self,
        template_id: int,
        is_active: bool,
    ) -> None:
        stmt = (
            update(NotificationTemplate)
            .where(NotificationTemplate.id == template_id)
            .values(is_active=is_active)
        )
        self.session.execute(stmt)
