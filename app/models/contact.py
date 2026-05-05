from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Contact(Base):
    __tablename__ = "contacts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    external_id: Mapped[str | None] = mapped_column(
        String,
        unique=True,
        nullable=True,
    )
    
    name: Mapped[str] = mapped_column(String, nullable=False)
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    
    contact_methods = relationship(
        "ContactMethod",
        back_populates="contact",
        cascade="all, delete-orphan",
    )
    groups = relationship(
        "Group",
        secondary="group_contacts",
        back_populates="contacts",
    )
