from datetime import datetime
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Integer

from models.appointments import AppointmentStatus, Appointments


class AppointmentsPublic(BaseModel):
    datetime_start: datetime
    datetime_end: datetime
    room_id: Integer


class AppointmenstSchema(AppointmentsPublic):
    id: Integer
    created_at: datetime
    reason: str
    status: AppointmentStatus
    applicant_id: Integer
    approver_id: Integer

    model_config = ConfigDict(from_attributes=True)
