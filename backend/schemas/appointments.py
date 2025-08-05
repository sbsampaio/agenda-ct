from datetime import datetime
from pydantic import BaseModel, ConfigDict

from models.appointments import AppointmentStatus, Appointments


class AppointmentsPublic(BaseModel):
    datetime_start: datetime
    datetime_end: datetime
    room_id: int


class AppointmenstSchema(AppointmentsPublic):
    id: int
    created_at: datetime
    reason: str
    status: AppointmentStatus
    applicant_id: int
    approver_id: int

    model_config = ConfigDict(from_attributes=True)
