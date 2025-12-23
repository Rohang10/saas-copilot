from pydantic import BaseModel, EmailStr,Field

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
