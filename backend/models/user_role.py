# --- third party imports ---
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# --- local imports ---
from ..base import Base
from .role import Role
from .user import User


# --- MODEL ---
class UserRole(Base):
    __tablename__ = "user_role"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        primary_key=True,
    )
    role_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("role.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        primary_key=True,
    )

    user = relationship("User", back_populates="user_role")
    role = relationship("Role", back_populates="user_role")

    def __repr__(self) -> str:
        return f"<UserRole(user_id={self.user_id}, role_id={self.role_id})>"
