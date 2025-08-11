# --- standard imports ---
from datetime import datetime
from enum import IntEnum

# --- third party imports ---
from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Text, TextClause
from sqlalchemy.orm import Mapped, mapped_column, relationship

# --- local imports ---
from ..settings.declarative_base import Base
from .room import Room
from .user import User


# --- ENUM ---
class AppointmentStatus(IntEnum):
    PENDING = 0
    APPROVED = 1
    REFUSED = 2
    CANCELED = 3


# --- MODEL ---
class Appointments(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=TextClause("CURRENT_TIMESTAMP"),
    )

    datetime_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    datetime_end: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[AppointmentStatus] = mapped_column(
        Enum(AppointmentStatus),
        nullable=False,
        comment="[0-Pending, 1-Approved, 2-Refused, 3-Canceled]",
    )

    applicant_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(User.id, ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    room_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(Room.id, ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    approver_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(User.id, ondelete="CASCADE"),
        index=True,
        nullable=True,
    )

    # --- relationships ---
    applicant = relationship(
        "User",
        foreign_keys=[applicant_id],
        back_populates="appointments_as_applicant",
    )
    approver = relationship(
        "User",
        foreign_keys=[approver_id],
        back_populates="appointments_as_approver",
    )
    room = relationship("Room", back_populates="appointments")

    def __repr__(self) -> str:
        return f"<Appointments(id={self.id}, applicant_id={self.applicant_id}, room_id={self.room_id})>"
