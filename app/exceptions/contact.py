from app.exceptions.base import ConflictError, NotFoundError


class ContactNotFoundError(NotFoundError):
    def __init__(self, contact_id: int):
        super().__init__(f"Contact {contact_id} not found")


class ContactAlreadyExistsError(ConflictError):
    def __init__(self):
        super().__init__("Contact already exists")
