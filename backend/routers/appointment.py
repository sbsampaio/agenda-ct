from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.database import get_session
from backend.models.user import User
from backend.models.appointment import Appointment
from backend.schemas import Message
from backend.schemas.appointment import AppointmentPublic
from backend.security import get_current_user
from backend.db_utils import is_admin


router = APIRouter(prefix="/appointments", tags=["appointments"])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.post("/", status_code=HTTPStatus.CREATED, response_model=AppointmentPublic)
def create_appointment(appointment: AppointmentPublic, session: Session, current_user: CurrentUser):

    conflicting_appointment = session.scalar(
        select(Appointment).where(
            Appointment.room_id == appointment.room_id,
            Appointment.status.in_([0, 1]),  # PENDING ou APPROVED
            Appointment.datetime_start < appointment.datetime_end,
            Appointment.datetime_end > appointment.datetime_start
        )
    )
    
    if conflicting_appointment:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Room is not available during the requested time period"
        )

    db_appointment = Appointment(
        reason=appointment.reason,
        room_id=appointment.room_id,
        datetime_start=appointment.datetime_start,
        datetime_end=appointment.datetime_end,
    )

    db_appointment.created_at = datetime.now()
    db_appointment.status = 0  # PENDING
    db_appointment.applicant_id = current_user.id
    db_appointment.approver_id = None

    session.add(db_appointment)
    session.commit()
    session.refresh(db_appointment)

    return db_appointment

@router.delete("/{appointment_id}", response_model=Message)
def cancel_appointment(appointment_id: int, session: Session, current_user: CurrentUser):
    appointment = session.get(Appointment, appointment_id)

    if not appointment:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Appointment not found")

    if appointment.applicant_id != current_user.id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Not authorized to cancel this appointment")

    appointment.status = 3  # CANCELED
    session.commit()

    return {"message": "Appointment cancelled successfully"}

@router.post("/{appointment_id}/approve", response_model=Message)
def approve_appointment(
    appointment_id: int, session: Session, current_user: CurrentUser
):
    appointment = session.get(Appointment, appointment_id)

    if not appointment:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Appointment not found")

    if not is_admin(current_user, session):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Admin role required to approve appointments")

    appointment.approver_id = current_user.id

    appointment.status = 1  # APPROVED
    session.commit()

    return {"message": "Appointment approved successfully"}

@router.post("/{appointment_id}/refuse", response_model=Message)
def refuse_appointment(
    appointment_id: int, session: Session, current_user: CurrentUser
):
    appointment = session.get(Appointment, appointment_id)

    if not appointment:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Appointment not found")

    if not is_admin(current_user, session):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Admin role required to refuse appointments")

    appointment.approver_id = current_user.id

    appointment.status = 2  # REFUSED
    session.commit()

    return {"message": "Appointment refused successfully"}