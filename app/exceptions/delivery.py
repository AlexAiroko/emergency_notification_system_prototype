from app.exceptions.base import NotFoundError


class DeliveryNotFoundError(NotFoundError):
    def __init__(self, delivery_id: int) -> None:
        super().__init__(f"Delivery {delivery_id} not found")
