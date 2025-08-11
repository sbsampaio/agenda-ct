from datetime import datetime
from pydantic import BaseModel, ConfigDict

from backend.models.appointments import AppointmentStatus, Appointments


class AppointmentsPublic(BaseModel):
    reason: str
    datetime_start: datetime
    datetime_end: datetime
    room_id: int


class AppointmentsSchema(AppointmentsPublic):
    id: int
    created_at: datetime
    status: AppointmentStatus
    applicant_id: int
    approver_id: int

    model_config = ConfigDict(from_attributes=True)
