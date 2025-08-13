from datetime import date, time, datetime

import pytest
from sqlalchemy import select

from backend.models.user import User
from backend.models.appointment import Appointment, AppointmentStatus
from backend.models.room import Room


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            id=1,
            first_name="alice", 
            last_name="wonderland", 
            password="secret", 
            email="alice@test.com"
        )
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.first_name == "alice"))

    assert user.id == 1
    assert user.first_name == "alice"
    assert user.last_name == "wonderland"
    assert user.password == "secret"
    assert user.email == "alice@test.com"
    assert user.created_at == time

def test_create_appointments(session, user):
    room = Room(
        id=1,
        name="Sala de Reunião CT 12",
        type="sala de reunião",
        location="CT 12, Térreo",
        capacity=10,
        description="Ar condicionado, projetor, quadro branco",
        active=True
    )
    session.add(room)
    session.commit()
    
    appointment = Appointment(
        id=1,
        reason="Reunião do CAI",
        datetime_start=datetime(2025, 8, 3, 18, 0, 0),
        datetime_end=datetime(2025, 8, 3, 20, 0, 0),
        status=AppointmentStatus.PENDING,
        applicant_id=user.id,
        room_id=room.id,
    )

    session.add(appointment)
    session.commit()

    saved_appointment = session.scalar(select(Appointment).where(Appointment.id == 1))

    assert saved_appointment.id == 1
    assert saved_appointment.reason == "Reunião do CAI"
    assert saved_appointment.datetime_start == datetime(2025, 8, 3, 18, 0, 0)
    assert saved_appointment.datetime_end == datetime(2025, 8, 3, 20, 0, 0)
    assert saved_appointment.status == AppointmentStatus.PENDING
    assert saved_appointment.applicant_id == user.id
    assert saved_appointment.room_id == room.id

def test_user_appointment_relationship(session, user: User):
    room = Room(
        id=1,
        name="Sala de Reunião 1",
        type="sala de reunião",
        location="CT 13, 3º Andar, Sala 301",
        capacity=10,
        description="Sala de reunião para 10 pessoas",
        active=True
    )
    session.add(room)
    session.commit()
    
    appointment = Appointment(
        id=1,
        reason="Reunião do CAI",
        datetime_start=datetime(2025, 8, 3, 18, 0, 0),
        datetime_end=datetime(2025, 8, 3, 20, 0, 0),
        status=AppointmentStatus.PENDING,
        applicant_id=user.id,
        room_id=room.id,
    )

    session.add(appointment)
    session.commit()
    session.refresh(user)

    user = session.scalar(select(User).where(User.id == user.id))

    assert user.appointments_as_applicant == [appointment]
