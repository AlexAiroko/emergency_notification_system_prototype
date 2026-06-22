from sqlalchemy.exc import IntegrityError

from app.db.uow import UnitOfWork
from app.exceptions.notification_template import TemplateAlreadyExistsError
from app.models.notification_template import NotificationTemplate


class NotificationTemplateService:
    def create_template(
        self,
        uow: UnitOfWork,
        body: str,
        name: str,
        subject: str | None = None,
        is_active: bool = True,
    ) -> NotificationTemplate:
        """
        Creates a new template.

        Business rules:
        - body must not be empty.
        """
        self._validate_body(body)

        try:
            return uow.template_repo.create(
                body=body,
                name=name,
                subject=subject,
                is_active=is_active,
            )
        except IntegrityError as exc:
            raise TemplateAlreadyExistsError() from exc

    def get_template(self, uow: UnitOfWork, template_id: int) -> NotificationTemplate | None:
        """
        Returns a template by ID or None.
        """
        return uow.template_repo.get(template_id)

    def get_many_templates(
        self,
        uow: UnitOfWork,
        limit: int = 20,
        offset: int = 0,
    ) -> list[NotificationTemplate]:
        """
        Returns a list of all templates.
        """
        return uow.template_repo.get_many(
            limit=limit,
            offset=offset,
        )

    def get_active_templates(
        self,
        uow: UnitOfWork,
        limit: int = 20,
        offset: int = 0,
    ) -> list[NotificationTemplate]:
        """
        Returns only active templates.
        """
        return uow.template_repo.get_active(
            limit=limit,
            offset=offset,
        )

    def update_template(
        self,
        uow: UnitOfWork,
        template_id: int,
        subject: str | None,
        body: str,
    ) -> None:
        """
        Updates the template's subject and body.

        Business rules:
        - body must not be empty.
        """
        self._validate_body(body)

        # The repository expects a string, so we replace None with an empty string.
        uow.template_repo.update_content(
            template_id=template_id,
            subject=subject or "",
            body=body,
        )

    def activate_template(self, uow: UnitOfWork, template_id: int) -> None:
        """
        Makes the template active.
        """
        uow.template_repo.activate(template_id)

    def deactivate_template(self, uow: UnitOfWork, template_id: int) -> None:
        """
        Makes the template inactive.
        """
        uow.template_repo.deactivate(template_id)

    def ensure_template_is_active(
        self,
        uow: UnitOfWork,
        template_id: int,
    ) -> NotificationTemplate:
        """
        Returns the template if it exists and is active.
        """
        template = uow.template_repo.get(template_id)

        if template is None:
            raise ValueError(f"Template {template_id} not found")

        if not template.is_active:
            raise ValueError(f"Template {template_id} is inactive")

        return template

    def _validate_body(self, body: str) -> None:
        """
        Проверяет, что body содержит непустой текст.
        """
        if not body or not body.strip():
            raise ValueError("Template body cannot be empty")
