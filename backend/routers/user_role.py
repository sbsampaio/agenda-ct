from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import get_session
from backend.models.user import User
from backend.models.user_role import UserRole
from backend.models.role import Role
from backend.schemas.user_role import UserRoleSchema
from backend.schemas.role import RoleSchema
from backend.schemas import Message
from backend.security import get_current_user

router = APIRouter(prefix="/user-role", tags=["user-role"])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserRoleSchema)
def assign_role_to_user(
    user_role: UserRoleSchema, 
    session: Session, 
):
    user = session.get(User, user_role.user_id)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="User not found"
        )
    
    role = session.get(Role, user_role.role_id)
    if not role:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="Role not found"
        )
    
    existing_user_role = session.scalar(
        select(UserRole).where(
            UserRole.user_id == user_role.user_id,
            UserRole.role_id == user_role.role_id
        )
    )
    
    if existing_user_role:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="User already has this role"
        )
    
    db_user_role = UserRole(
        user_id=user_role.user_id,
        role_id=user_role.role_id
    )
    
    session.add(db_user_role)
    session.commit()
    session.refresh(db_user_role)
    
    return db_user_role


@router.delete("/{user_id}/{role_id}", response_model=Message)
def remove_role_from_user(
    user_id: int, 
    role_id: int, 
    session: Session, 
):
    
    user_role = session.scalar(
        select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id
        )
    )
    
    if not user_role:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User role relationship not found"
        )
    
    session.delete(user_role)
    session.commit()
    
    return {"message": "Role removed from user successfully"}

@router.get("/{user_id}/has-role/{role_id}", response_model=dict)
def check_user_has_role(
    user_id: int, 
    role_id: int, 
    session: Session, 
):
    
    user_role = session.scalar(
        select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id
        )
    )
    
    return {"has_role": user_role is not None}