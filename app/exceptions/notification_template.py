from app.exceptions.base import ConflictError, NotFoundError, ValidationError


class TemplateNotFoundError(NotFoundError):
    def __init__(self, template_id: int):
        super().__init__(f"Template {template_id} not found")


class TemplateAlreadyExistsError(ConflictError):
    def __init__(self):
        super().__init__("Template already exists")


class TemplateInactiveError(ValidationError):
    def __init__(self, template_id: int):
        super().__init__(f"Template {template_id} is inactive")


class TemplateBodyEmptyError(ValidationError):
    def __init__(self):
        super().__init__("Template body cannot be empty")
