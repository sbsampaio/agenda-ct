from datetime import datetime
from pydantic import BaseModel, ConfigDict

from backend.models.appointment import AppointmentStatus, Appointment


class AppointmentPublic(BaseModel):
    reason: str
    datetime_start: datetime
    datetime_end: datetime
    room_id: int


class AppointmentSchema(AppointmentPublic):
    id: int
    created_at: datetime
    status: AppointmentStatus
    applicant_id: int
    approver_id: int

    model_config = ConfigDict(from_attributes=True)
