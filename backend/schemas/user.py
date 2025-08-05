from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str

class UserSchema(UserBase):
    password: str
    
class UserPublic(BaseModel):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)