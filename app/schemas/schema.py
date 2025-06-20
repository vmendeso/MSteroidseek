from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)