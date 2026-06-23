from pydantic import BaseModel, ConfigDict


class NotificationTemplateCreate(BaseModel):
    name: str
    subject: str | None = None
    body: str
    is_active: bool = True


class NotificationTemplateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    subject: str | None
    body: str
    is_active: bool


class NotificationTemplateUpdate(BaseModel):
    subject: str | None = None
    body: str
