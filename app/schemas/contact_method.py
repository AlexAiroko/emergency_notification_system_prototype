from pydantic import BaseModel, ConfigDict

from app.models.contact_method import ChannelType


class ContactMethodCreate(BaseModel):
    channel: ChannelType
    address: str


class ContactMethodUpdate(BaseModel):
    channel: ChannelType
    address: str
    is_active: bool


class ContactMethodResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    contact_id: int
    channel: ChannelType
    address: str
    is_active: bool
