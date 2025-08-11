# --- third party imports ---
from sqlalchemy import BigInteger, Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

# --- local imports ---
from ..base import Base

# --- CONSTANTS ---
NAME_LEN = 100
TYPE_LEN = 50
LOCATION_LEN = 255


# --- MODEL ---
class Room(Base):
    __tablename__ = "room"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(String(NAME_LEN), nullable=False)
    type: Mapped[str] = mapped_column(
        String(TYPE_LEN),
        nullable=False,
        comment="ex: laboratório, sala de reunião, auditório",
    )

    location: Mapped[str] = mapped_column(
        String(LOCATION_LEN),
        nullable=False,
        comment="ex: CT 13, 3º Andar, Sala 301",
    )
    capacity: Mapped[int] = mapped_column(BigInteger, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # --- relationships ---
    appointments = relationship("Appointments", back_populates="appointment_room", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Room(id={self.id}, name={self.name})>"
