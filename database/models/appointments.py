from datetime import datetime
from enum import IntEnum

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Text, TextClause
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..settings.declarative_base import Base
from .room import Room
from .user import User


class AppointmentStatus(IntEnum):
    PENDING = 0
    APPROVED = 1
    REFUSED = 2
    CANCELED = 3


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
    )

    applicant = relationship("User", back_populates="appointment")
    room = relationship("Room", back_populates="appointment")

    def __repr__(self) -> str:
        return f"<Appointments(id={self.id}, applicant_id={self.applicant_id}, room_id={self.room_id})>"
