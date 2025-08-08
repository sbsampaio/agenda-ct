# --- third party imports ---
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# --- local imports ---
from ..base import Base

# --- CONSTANTS ---
NAME_LEN = 50


# --- MODEL ---
class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(String(NAME_LEN), nullable=False)

    user_role = relationship(
        "UserRole",
        back_populates="role",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name={self.name})>"
