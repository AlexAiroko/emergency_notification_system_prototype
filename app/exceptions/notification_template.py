from app.exceptions.base import ConflictError, NotFoundError, ValidationError


class TemplateNotFoundError(NotFoundError):
    code = "template_not_found"

    def __init__(self, template_id: int):
        super().__init__(f"Template {template_id} not found")


class TemplateAlreadyExistsError(ConflictError):
    code = "template_already_exists"

    def __init__(self):
        super().__init__("Template already exists")


class TemplateInactiveError(ValidationError):
    code = "template_inactive"

    def __init__(self, template_id: int):
        super().__init__(f"Template {template_id} is inactive")


class TemplateBodyEmptyError(ValidationError):
    code = "template_body_empty"

    def __init__(self):
        super().__init__("Template body cannot be empty")
