from app.repositories.contact import ContactRepository
from app.repositories.notification import NotificationRepository
from app.repositories.delivery import DeliveryRepository
from app.repositories.group import GroupRepository
from app.repositories.notification_template import NotificationTemplateRepository


REPOSITORIES = {
    "notification_repo": NotificationRepository,
    "deliverie_repo": DeliveryRepository,
    "group_repo": GroupRepository,
    "template_repo": NotificationTemplateRepository,
    "contact_repo": ContactRepository,
}
