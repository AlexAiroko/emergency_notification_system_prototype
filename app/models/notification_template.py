from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class NotificationTemplate(Base):
    __tablename__ = "notification_templates"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )
    
    subject: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    
    body: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    
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
