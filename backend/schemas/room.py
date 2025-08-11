from pydantic import BaseModel, ConfigDict

class RoomPublic(BaseModel):
    name: str
    type: str
    location: str
    capacity: int
    description: str

class RoomSchema(RoomPublic):
    id: int
    active: bool

    model_config = ConfigDict(from_attributes=True)
