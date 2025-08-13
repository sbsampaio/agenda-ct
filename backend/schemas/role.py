from pydantic import BaseModel, ConfigDict


class RoleCreate(BaseModel):
    name: str


class RoleSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
