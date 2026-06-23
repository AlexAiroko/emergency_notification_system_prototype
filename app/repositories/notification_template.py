from app.models.notification_template import NotificationTemplate
from app.repositories.active import ActiveRepository


class NotificationTemplateRepository(ActiveRepository):
    model = NotificationTemplate
