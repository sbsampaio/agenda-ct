from pydantic import BaseModel, ConfigDict


class UserRoleSchema(BaseModel):
    user_id: int
    role_id: int

    model_config = ConfigDict(from_attributes=True)
