from datetime import datetime
from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger

from models.appointments import AppointmentStatus, Appointments


class AppointmentsPublic(BaseModel):
    datetime_start: datetime
    datetime_end: datetime
    room_id: BigInteger


class AppointmenstSchema(AppointmentsPublic):
    id: BigInteger
    created_at: datetime
    reason: str
    status: AppointmentStatus
    applicant_id: BigInteger
    approver_id: BigInteger

    model_config = ConfigDict(from_attributes=True)
