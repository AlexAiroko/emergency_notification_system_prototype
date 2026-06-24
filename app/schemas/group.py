from pydantic import BaseModel, ConfigDict

from app.schemas.contact import ContactResponse


class GroupCreate(BaseModel):
    name: str


class GroupUpdate(BaseModel):
    name: str


class GroupResponse(BaseModel):
    id: int
    name: str
    is_active: bool


class GroupWithContactsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    is_active: bool
    
    contacts: list[ContactResponse]
