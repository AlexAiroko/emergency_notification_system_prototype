from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class GroupContact(Base):
    __tablename__ = "group_contacts"
    
    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id", ondelete="CASCADE"),
        primary_key=True,
    )
    
    contact_id: Mapped[int] = mapped_column(
        ForeignKey("contacts.id", ondelete="CASCADE"),
        primary_key=True,
    )
