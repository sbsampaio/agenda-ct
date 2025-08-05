from pydantic import BaseModel, ConfigDict


class RoomSchema(BaseModel):
    id: int
    name: str
    type: str
    location: str
    capacity: int
    description: str
    active: bool

    model_config = ConfigDict(from_attributes=True)
