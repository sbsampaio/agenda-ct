from typing import Annotated
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import get_session
from backend.models.user import User
from backend.models.user_role import UserRole
from backend.security import get_current_user

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def assign_role_to_user_internal(user_id: int, role_id: int, session: Session):
    existing_user_role = session.scalar(
        select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id
        )
    )
    
    if existing_user_role:
        return False
    
    db_user_role = UserRole(user_id=user_id, role_id=role_id)
    session.add(db_user_role)
    session.commit()
    
    return True


def remove_role_from_user_internal(user_id: int, role_id: int, session: Session):
    user_role = session.scalar(
        select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id
        )
    )
    
    if not user_role:
        return False
    
    session.delete(user_role)
    session.commit()
    
    return True


def check_user_has_role_internal(user_id: int, role_id: int, session: Session):
    user_role = session.scalar(
        select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id
        )
    )
    
    return user_role is not None