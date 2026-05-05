import enum

from sqlalchemy import Boolean, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ChannelType(enum.Enum):
    SMS = "sms"
    EMAIL = "email"
    TELEGRAM = "telegram"


class ContactMethod(Base):
    __tablename__ = "contact_methods"
    
    id: Mapped[int] = mapped_column(primary_key=True)

    contact_id: Mapped[int] = mapped_column(
        ForeignKey("contacts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    channel: Mapped[ChannelType] = mapped_column(
        Enum(
            ChannelType,
            name="channel_type",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
        ),
        nullable=False,
    )
    
    address: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    
    contact = relationship("Contact", back_populates="contact_methods")
