from pydantic import BaseModel, ConfigDict


class ContactCreate(BaseModel):
    name: str
    external_id: str | None = None


class ContactUpdate(BaseModel):
    name: str


class ContactResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    external_id: str | None
    is_active: bool
