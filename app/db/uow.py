from app.db.repositories_registry import REPOSITORIES
from app.db.session import session_maker
from app.repositories.contact import ContactRepository
from app.repositories.contact_method import ContactMethodRepository
from app.repositories.delivery import DeliveryRepository
from app.repositories.group import GroupRepository
from app.repositories.notification import NotificationRepository
from app.repositories.notification_template import NotificationTemplateRepository


class UnitOfWork:
    template_repo: NotificationTemplateRepository
    notification_repo: NotificationRepository
    delivery_repo: DeliveryRepository
    group_repo: GroupRepository
    contact_repo: ContactRepository
    contact_method_repo: ContactMethodRepository
    
    def __init__(self):
        self.session = None

    def __enter__(self):
        self.session = session_maker()
        self.transaction = self.session.begin()
        self.transaction.__enter__()

        return self

    def __exit__(self, exc_type, exc, tb):
        self.transaction.__exit__(exc_type, exc, tb)
        self.session.close()
    
    def __getattr__(self, name: str):
        if name in REPOSITORIES:
            repo_class = REPOSITORIES[name]

            repo = repo_class(self.session)
            setattr(self, name, repo) # save repo

            return repo

        raise AttributeError(f"No repository: {name}")
