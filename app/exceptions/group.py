from app.exceptions.base import ConflictError, NotFoundError


class GroupNotFoundError(NotFoundError):
    def __init__(self, group_id: int):
        super().__init__(f"Group {group_id} not found")


class GroupAlreadyExistsError(ConflictError):
    def __init__(self):
        super().__init__("Group already exists")
