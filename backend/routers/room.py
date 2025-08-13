from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.database import get_session
from backend.db_utils import is_admin
from backend.models.user import User
from backend.schemas import Message
from backend.schemas.room import RoomPublic
from backend.security import get_current_user
from backend.models.room import Room


router = APIRouter(prefix="/room", tags=["room"])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.post("/", status_code=HTTPStatus.CREATED, response_model=RoomPublic)
def create_room(room: RoomPublic, session: Session, current_user: CurrentUser):

    db_room = Room(
        name=room.name,
        type=room.type,
        capacity=room.capacity,
        location=room.location,
        description=room.description,
    )

    db_room.active = True

    session.add(db_room)
    session.commit()
    session.refresh(db_room)

    return db_room

@router.delete("/{room_id}", response_model=Message)
def deactivate_room(room_id: int, session: Session, current_user: CurrentUser):
    room = session.get(Room, room_id)

    if not room:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Room not found")

    if not is_admin(current_user, session):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Not authorized to deactivate this room")

    room.active = False
    session.commit()

    return {"message": "Room deactivated successfully"}

