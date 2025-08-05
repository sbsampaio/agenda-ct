# --- standard imports ---
from datetime import datetime

# --- third party imports ---
from sqlalchemy import BigInteger, DateTime, String, TextClause
from sqlalchemy.orm import Mapped, mapped_column, relationship

# --- local imports ---
from database.settings.declarative_base import Base

# --- CONSTANTS ---
EMAIL_LEN = 150
PASSWORD_LEN = 255
NAME_LEN = 50


# --- MODEL ---
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=TextClause("CURRENT_TIMESTAMP"),
    )

    email: Mapped[str] = mapped_column(String(EMAIL_LEN), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(PASSWORD_LEN), nullable=False)

    first_name: Mapped[str] = mapped_column(String(NAME_LEN), nullable=False)
    last_name: Mapped[str] = mapped_column(String(NAME_LEN), nullable=False)

    # --- relationships ---
    user_role = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    appointments_as_applicant = relationship(
        "Appointment",
        foreign_keys="Appointment.applicant_id",
        back_populates="applicant",
    )
    appointments_as_approver = relationship(
        "Appointment",
        foreign_keys="Appointment.approver_id",
        back_populates="approver",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
